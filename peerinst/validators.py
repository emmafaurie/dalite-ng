import logging
from html import unescape

import bleach
from django.core.validators import BaseValidator, MinLengthValidator
from django.utils.translation import ngettext_lazy
from langdetect import DetectorFactory, LangDetectException, detect_langs
from profanity_check import predict_prob

from .profanity import profanity

DetectorFactory.seed = 0
validation_logger = logging.getLogger("validation")


def html_to_text(value):
    """Remove all tags and unescape HTML entities"""
    return unescape(
        " ".join(bleach.clean(value, tags=[], strip=True).strip().split())
    )


class MinWordsValidator(MinLengthValidator):
    message = ngettext_lazy(
        "Ensure this value has at least %(limit_value)d word (it has %(show_value)d).",
        "Ensure this value has at least %(limit_value)d words (it has %(show_value)d).",
        "limit_value",
    )
    code = "min_words"

    def clean(self, text):
        cleaned_text = html_to_text(text)
        result = len(str(cleaned_text).split())
        validation_logger.info(f"Word count: {result} for '{text}'")
        return result


class NoProfanityValidator(BaseValidator):
    """
    The profanity check is twofold:

    - alt-profanity-check is a machine-learning model based on a 200k corpus of human-
      labeled samples and no explicit banned words list.  It is highly performant,
      but won't detect less common variants, like sh1tty.
    - better-profanity has a hard-coded wordlist and is able to check a wider range of
      variants.

    We check probability from alt-profanity-check is less than limit_value and that
    better-profanity results False.

    The better-profanity wordlist is quite conservative and some terms may need to be
    whitelisted.

    Both packages are English only.  Extended supported for other languages is required.

    The limit_value arg defines the probability threshold below which the passed text
    must be to pass.
    """

    message = ngettext_lazy("", "")
    code = "no_profanity"

    def compare(self, a, b):
        # True results in a ValidationError
        result = a[0] > b or a[1]
        if result:
            validation_logger.info(
                f"Profanity scores: [{a[0]}, {a[1]}] for '{a[2]}'"
            )
        return result

    def clean(self, text):
        # Return a tuple with results from both models
        cleaned_text = html_to_text(text)
        return (
            predict_prob([cleaned_text])[0],
            profanity.contains_profanity(cleaned_text),
            text,
        )


class EnglishFrenchValidator(BaseValidator):
    """
    The language check asserts that the probability of a string belonging to either
    French or English is above the required limit value.
    """

    message = ngettext_lazy("", "")
    code = "english_or_french"

    def compare(self, a, b):
        # True results in a ValidationError
        result = a[0] < b and a[1] < b
        if result:
            validation_logger.info(
                f"Language probabilities: [{a[0]}, {a[1]}] for '{a[2]}'"
            )
        return result

    def clean(self, text):
        # Return a tuple with results English and French
        cleaned_text = html_to_text(text)
        validation_logger.info(cleaned_text)
        try:
            detected_languages = detect_langs(cleaned_text)
        except LangDetectException:
            detected_languages = []

        dl_as_dict = {
            result.lang: result.prob for result in detected_languages
        }
        return (dl_as_dict.get("en", 0), dl_as_dict.get("fr", 0), text)
