from unittest.mock import patch

from better_profanity.better_profanity import Profanity


class WhitespaceSeparatedProfanity(Profanity):
    """
    The original Profanity class functions exactly as needed but it imports
    a utility function to look for swear words formed across word separators.
    Tests show that the strategy results in a lot of false positives for
    the kinds of rationales students in Science write.

    We want to keep the original class and overwrite just this utility function.
    """

    @patch(
        "better_profanity.better_profanity.any_next_words_form_swear_word",
        lambda cur_word, next_words_indices, censor_words: (False, -1),
    )
    def _hide_swear_words(self, text, censor_char):
        return super()._hide_swear_words(text, censor_char)


profanity = WhitespaceSeparatedProfanity()

# Default profanity list from better_profanity includes many biological terms.
# Here we whitelist a selection of them; to be revisited.
profanity.load_censor_words(
    whitelist_words=[
        "anus",
        "bastard",
        "breasts",
        "busty",
        "clitoris",
        "crap",
        "crotch",
        "damn",
        "dogging",
        "drunk",
        "erect",
        "erection",
        "erotic",
        "erotism",
        "extasy",
        "facial",
        "fanny",
        "fart",
        "fat",
        "floozy",
        "fondle",
        "foreskin",
        "gay",
        "gays",
        "god",
        "goddam",
        "goddamn",
        "goddamned",
        "goddammit",
        "gonad",
        "hell",
        "hemp",
        "heroin",
        "herpes",
        "hitler",
        "hiv",
        "homoerotic",
        "horny",
        "hump",
        "humped",
        "humping",
        "hymen",
        "inbred",
        "incest",
        "jerk",
        "junkie",
        "junky",
        "kill",
        "kinky",
        "knob",
        "labia",
        "leper",
        "lesbians",
        "loin",
        "loins",
        "lust",
        "lusting",
        "masochist",
        "masterbate",
        "masterbating",
        "masterbation",
        "masterbations",
        "masturbate",
        "masturbating",
        "masturbation",
        "maxi",
        "menses",
        "menstruate",
        "menstruation",
        "meth",
        "molest",
        "moron",
        "murder",
        "naked",
        "nazi",
        "nazism",
        "nipple",
        "nipples",
        "nude",
        "nudes",
        "omg",
        "opiate",
        "opium",
        "oral",
        "orally",
        "organ",
        "orgasm",
        "ovary",
        "ovum",
        "ovums",
        "panties",
        "panty",
        "pedophile",
        "pedophilia",
        "pedophiliac",
        "pee",
        "penetrate",
        "penetration",
        "penile",
        "penis",
        "perversion",
        "peyote",
        "phallic",
        "pimp",
        "piss",
        "pissed",
        "playboy",
        "pms",
        "porn",
        "porno",
        "pornography",
        "pornos",
        "pot",
        "prostitute",
        "prude",
        "pubic",
        "queer",
        "queers",
        "racy",
        "rape",
        "raped",
        "raper",
        "raping",
        "rapist",
        "raunch",
        "rectal",
        "rectum",
        "retarded",
        "rump",
        "sadism",
        "sadist",
        "scantily",
        "screw",
        "screwed",
        "screwing",
        "scrotum",
        "scum",
        "seduce",
        "semen",
        "sex",
        "sexual",
        "slave",
        "sleaze",
        "sleazy",
        "slope",
        "smut",
        "smutty",
        "snatch",
        "sniper",
        "sob",
        "sperm",
        "steamy",
        "stoned",
        "strip",
        "strip club",
        "stripclub",
        "stroke",
        "stupid",
        "suck",
        "sucked",
        "sucking",
        "tampon",
        "tawdry",
        "teat",
        "teets",
        "testes",
        "testical",
        "testicle",
        "threesome",
        "thrust",
        "thug",
        "tinkle",
        "tramp",
        "transsexual",
        "trashy",
        "tush",
        "ugly",
        "undies",
        "unwed",
        "urinal",
        "urine",
        "uterus",
        "vagina",
        "valium",
        "viagra",
        "virgin",
        "vixen",
        "vodka",
        "vomit",
        "voyeur",
        "vulgar",
        "vulva",
        "wad",
        "weed",
        "weiner",
        "weirdo",
        "womb",
    ]
)
