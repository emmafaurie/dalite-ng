from datetime import date, datetime

import bleach
import pytz
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from peerinst.templatetags.bleach_html import STRICT_TAGS

from .models import (
    Assignment,
    Category,
    Discipline,
    Question,
    StudentGroup,
    StudentGroupAssignment,
    Teacher,
)
from .validators import (
    EnglishFrenchValidator,
    MinWordsValidator,
    NoProfanityValidator,
)


class NonStudentAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if hasattr(user, "student"):
            raise ValidationError(
                _("Students cannot login via username and password"),
                code="no_students",
            )


class TeacherPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        return User.objects.filter(
            email__iexact=email, is_active=True, teacher__isnull=False
        ).filter(
            Q(password__isnull=True)
            | ~Q(password__startswith=UNUSABLE_PASSWORD_PREFIX)
        )


class RichTextRationaleField(forms.CharField):
    widget = TinyMCE(
        attrs={"cols": 100, "rows": 7},
        mce_attrs={
            "plugins": "advlist,lists,charmap,preview,wordcount",
            "toolbar": "undo redo | charmap | bold italic underline subscript "
            "superscript | bullist numlist | removeformat",
        },
    )
    default_error_messages = {
        "required": _("Please provide a rationale for your choice.")
    }
    default_validators = [
        MinWordsValidator(
            4,
            _("Please provide a more detailed rationale for your choice."),
        ),
        NoProfanityValidator(
            0.7,
            _(
                "The language filter has labeled this as possibly toxic or profane; please rephrase your rationale."  # noqa
            ),
        ),
        EnglishFrenchValidator(
            0.5,
            _("Please clarify what you've written."),
        ),
    ]

    def to_python(self, value):
        """Remove all unsafe input"""
        return bleach.clean(
            super().to_python(value),
            tags=STRICT_TAGS,
            strip=True,
        )


class FirstAnswerForm(forms.Form):
    """Form to select one of the answer choices and enter a rationale."""

    error_css_class = "validation-error"

    first_answer_choice = forms.ChoiceField(
        label=_("Choose one of these answers:"),
        widget=forms.RadioSelect,
        error_messages={
            "required": _("Please make sure to select an answer choice.")
        },
    )
    rationale = RichTextRationaleField()

    def __init__(self, answer_choices, *args, **kwargs):
        choice_texts = [
            mark_safe(
                f"<div class='flex-label'><div><strong>{pair[0]}.</strong></div><div>{pair[1]}</div></div>"  # noqa E501
            )
            for pair in answer_choices
        ]
        self.base_fields["first_answer_choice"].choices = enumerate(
            choice_texts, 1
        )
        forms.Form.__init__(self, *args, **kwargs)


class RationaleOnlyForm(forms.Form):

    error_css_class = "validation-error"

    rationale = RichTextRationaleField()
    datetime_start = forms.CharField(
        widget=forms.HiddenInput(), initial=datetime.now(pytz.utc)
    )

    def __init__(self, answer_choices, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)


class ReviewAnswerForm(forms.Form):
    """Form on the answer review page."""

    error_css_class = "validation-error"

    second_answer_choice = forms.ChoiceField(
        label="", widget=forms.RadioSelect
    )

    shown_rationales = []

    RATIONALE_CHOICE = "rationale_choice"

    def __init__(self, rationale_choices, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        answer_choices = []
        rationale_choice_fields = []
        show_more_counters = []
        show_more_labels = []
        rationale_id_list = []
        for i, (choice, label, rationales) in enumerate(rationale_choices):
            rationales = [
                (id_ if id_ is not None else "None", rationale)
                for id_, rationale in rationales
            ]
            rationale_ids = [
                (id_ if id_ is not None else "None")
                for id_, rationale in rationales
            ]

            field_name = f"{self.RATIONALE_CHOICE}_{i}"
            self.fields[field_name] = forms.ChoiceField(
                label="",
                required=False,
                widget=forms.RadioSelect,
                choices=rationales,
            )
            show_more_field_name = f"show-more-counter-{str(i + 1)}"
            self.fields[show_more_field_name] = forms.IntegerField(
                required=False, initial=2
            )
            show_more_counters.append(self[show_more_field_name])
            show_more_labels.append(show_more_field_name)
            answer_choices.append((choice, label))
            rationale_choice_fields.append(self[field_name])
            rationale_id_list.append(rationale_ids)
        self.fields["second_answer_choice"].choices = answer_choices
        self.rationale_groups = list(
            zip(
                self["second_answer_choice"],
                rationale_choice_fields,
                show_more_counters,
                show_more_labels,
                rationale_id_list,
            )
        )

    def clean(self):
        cleaned_data = forms.Form.clean(self)
        shown_rationales = []
        if cleaned_data is not None:
            for (
                _answer_choice,
                _rationale_choice_field,
                _show_more_counter,
                label,
                rationale_ids,
            ) in self.rationale_groups:
                shown_rationales.extend(
                    rationale_ids[i]
                    for i in (
                        range(cleaned_data[label])
                        if cleaned_data[label]
                        else range(min(2, len(rationale_ids)))
                    )
                    if (
                        rationale_ids[i] is not None
                        and rationale_ids[i] != "None"
                    )
                )

        self.shown_rationales = shown_rationales or None
        rationale_choices = [
            value
            for key, value in cleaned_data.items()
            if key.startswith(self.RATIONALE_CHOICE)
        ]
        if sum(map(bool, rationale_choices)) != 1:
            # This should be prevented by the UI on the client side, so this
            # check is mostly to
            # protect against bugs and people transferring made-up data.
            raise forms.ValidationError(
                _("Please select exactly one rationale.")
            )
        chosen_rationale_id = next(
            value for value in rationale_choices if value
        )
        cleaned_data.update(chosen_rationale_id=chosen_rationale_id)
        return cleaned_data


class SequentialReviewForm(forms.Form):
    """Form to vote on a single rationale."""

    def clean(self):
        cleaned_data = forms.Form.clean(self)
        if "upvote" in self.data:
            cleaned_data["vote"] = "up"
        elif "downvote" in self.data:
            cleaned_data["vote"] = "down"
        else:
            raise forms.ValidationError(_("Please vote up or down."))
        return cleaned_data


class AssignmentCreateForm(forms.ModelForm):
    """Simple form to create a new Assignment"""

    class Meta:
        model = Assignment
        fields = [
            "identifier",
            "title",
            "description",
            "intro_page",
            "conclusion_page",
        ]
        widgets = {
            "description": TinyMCE(),
            "intro_page": TinyMCE(),
            "conclusion_page": TinyMCE(),
        }


class AssignmentMultiselectForm(forms.Form):
    def __init__(self, user=None, question=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove assignments with question and assignments with student
        # answers
        queryset = (
            user.assignment_set.all() if user else Assignment.objects.all()
        )
        num_student_rationales = Count(
            "answer", filter=~Q(answer__user_token="")
        )

        if question:
            queryset = (
                queryset.annotate(
                    num_student_rationales=num_student_rationales
                )
                .filter(Q(num_student_rationales=0))
                .exclude(questions=question)
            )
        else:
            queryset = queryset.annotate(
                num_student_rationales=num_student_rationales
            ).filter(Q(num_student_rationales=0))

        # Add queryset to form object to keep logic in one spot
        self.queryset = queryset

        self.fields["assignments"] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            required=False,
            label=_("Assignments"),
            help_text=_(
                "Optional. Select assignments to add this question. You can "
                "select multiple assignments. Assignments that this question "
                "is already a part of will not appear in list."
            ),
        )


class TeacherAssignmentsForm(forms.Form):
    """Simple form to help update teacher assignments"""

    assignment = forms.ModelChoiceField(queryset=Assignment.objects.all())


class TeacherGroupsForm(forms.Form):
    """Simple form to help update teacher groups"""

    group = forms.ModelChoiceField(queryset=StudentGroup.objects.all())


class SignUpForm(ModelForm):
    """Form to register a new user (teacher) with e-mail address.

    The clean method is overridden to add basic password validation."""

    email = forms.EmailField()

    url = forms.URLField(
        label=_("Website"),
        initial="http://",
        max_length=200,
        help_text=_(
            "Please provide an institutional url listing yourself as a "
            "faculty member and showing your e-mail address."
        ),
    )

    class Meta:
        model = User
        fields = ["email", "username"]


class ActivateForm(forms.Form):
    """Form to activate a User and initialize as Teacher, if indicated."""

    is_teacher = forms.BooleanField(required=False)
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=False)
    )


class EmailForm(forms.Form):
    """Form for user email address"""

    email = forms.EmailField()


class AddRemoveQuestionForm(forms.Form):
    q = forms.ModelChoiceField(queryset=Question.objects.all())


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ["title"]


class DisciplineSelectForm(forms.Form):
    discipline = forms.ModelChoiceField(
        queryset=Discipline.objects.all(),
        help_text=_(
            "Optional. Select the discipline to which this item should "
            "be associated."
        ),
    )


class DisciplinesSelectForm(forms.Form):
    disciplines = forms.ModelMultipleChoiceField(
        queryset=Discipline.objects.all()
    )


class CategorySelectForm(forms.Form):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        help_text=_(
            "Type to search and select at least one category for this "
            "question. You can select multiple categories."
        ),
    )


class ReportSelectForm(forms.Form):

    student_groups = forms.ModelMultipleChoiceField(
        label=_("Choose which groups to include in report:"),
        widget=forms.CheckboxSelectMultiple,
        queryset=StudentGroup.objects.none(),
    )

    assignments = forms.ModelMultipleChoiceField(
        label=_("Choose which assignments to include in report:"),
        widget=forms.CheckboxSelectMultiple,
        queryset=Assignment.objects.none(),
    )

    def __init__(self, teacher_username, *args, **kwargs):
        self.base_fields["assignments"].queryset = Teacher.objects.get(
            user__username=teacher_username
        ).assignments.all()
        self.base_fields["student_groups"].queryset = Teacher.objects.get(
            user__username=teacher_username
        ).current_groups.all()
        forms.Form.__init__(self, *args, **kwargs)


class AnswerChoiceForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE())


def current_year():
    return date.today().year


def year_choices():
    return [(i, i) for i in range(2015, current_year() + 2)]


class StudentGroupCreateForm(forms.ModelForm):
    """Simple form to create a new group"""

    year = forms.TypedChoiceField(
        coerce=int, choices=year_choices, initial=current_year
    )

    class Meta:
        model = StudentGroup
        fields = [
            "title",
            "name",
            "year",
            "semester",
            "discipline",
            "institution",
        ]


class StudentGroupUpdateForm(forms.ModelForm):
    """Simple form to create a new group"""

    year = forms.TypedChoiceField(
        coerce=int, choices=year_choices, initial=current_year
    )

    class Meta:
        model = StudentGroup
        fields = [
            "title",
            "student_id_needed",
            "year",
            "semester",
            "discipline",
        ]
        read_only_fields = ["name"]


class StudentGroupAssignmentForm(ModelForm):
    group = forms.ModelChoiceField(
        queryset=StudentGroup.objects.filter(
            Q(mode_created=StudentGroup.STANDALONE)
            | Q(mode_created=StudentGroup.LTI_STANDALONE)
        ),
        empty_label=None,
        help_text=_(
            "Note: You can only distribute assignments to groups created from within myDALITE, or using the LTI-Standalone launch url in your LMS.  To distribute one question at a time to your students  via an LMS (like Moodle), use the 'Distribute via LMS' option."  # noqa E501
        ),
    )

    class Meta:
        model = StudentGroupAssignment
        fields = ("group", "due_date", "show_correct_answers")


class StudentGroupAssignmentManagementForm(forms.Form):
    group_assignment = forms.ModelChoiceField(
        queryset=StudentGroupAssignment.objects.all()
    )
