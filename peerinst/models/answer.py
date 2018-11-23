# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .assignment import Assignment
from .question import GradingScheme, Question


class AnswerChoice(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField(_("Text"), max_length=500)
    correct = models.BooleanField(_("Correct?"))

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ["id"]
        verbose_name = _("answer choice")
        verbose_name_plural = _("answer choices")


class Answer(models.Model):
    question = models.ForeignKey(Question)
    assignment = models.ForeignKey(Assignment, blank=True, null=True)
    first_answer_choice = models.PositiveSmallIntegerField(
        _("First answer choice")
    )
    rationale = models.TextField(_("Rationale"))
    second_answer_choice = models.PositiveSmallIntegerField(
        _("Second answer choice"), blank=True, null=True
    )
    chosen_rationale = models.ForeignKey("self", blank=True, null=True)
    user_token = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Corresponds to the user's username."),
    )
    show_to_others = models.BooleanField(_("Show to others?"), default=True)
    expert = models.BooleanField(
        _("Expert rationale?"),
        default=False,
        help_text=_("Whether this answer is a pre-seeded expert rationale."),
    )
    time = models.DateTimeField(blank=True, null=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def first_answer_choice_label(self):
        return self.question.get_choice_label(self.first_answer_choice)

    first_answer_choice_label.short_description = _("First answer choice")
    first_answer_choice_label.admin_order_field = "first_answer_choice"

    def second_answer_choice_label(self):
        return self.question.get_choice_label(self.second_answer_choice)

    second_answer_choice_label.short_description = _("Second answer choice")
    second_answer_choice_label.admin_order_field = "second_answer_choice"

    def __unicode__(self):
        return unicode(
            _("{} for question {}").format(self.id, self.question.title)
        )

    def get_grade(self):
        """ Compute grade based on grading scheme of question. """
        if self.question.grading_scheme == GradingScheme.STANDARD:
            # Standard grading scheme: Full score if second answer is correct
            correct = self.question.is_correct(self.second_answer_choice)
            return float(correct)
        else:
            # Advanced grading scheme: Partial scores for individual answers
            grade = 0.0
            if self.question.is_correct(self.first_answer_choice):
                grade += 0.5
            if self.question.is_correct(self.second_answer_choice):
                grade += 0.5
            return grade

    def show_chosen_rationale(self):
        if self.chosen_rationale:
            return self.chosen_rationale.rationale
        else:
            return None

    show_chosen_rationale.short_description = "Display chosen rationale"


class AnswerVote(models.Model):
    """Vote on a rationale with attached fake attribution."""

    answer = models.ForeignKey(Answer)
    assignment = models.ForeignKey(Assignment)
    user_token = models.CharField(max_length=100)
    fake_username = models.CharField(max_length=100)
    fake_country = models.CharField(max_length=100)
    UPVOTE = 0
    DOWNVOTE = 1
    FINAL_CHOICE = 2
    VOTE_TYPE_CHOICES = (
        (UPVOTE, "upvote"),
        (DOWNVOTE, "downvote"),
        (FINAL_CHOICE, "final_choice"),
    )
    vote_type = models.PositiveSmallIntegerField(
        _("Vote type"), choices=VOTE_TYPE_CHOICES
    )


class RationaleOnlyManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)

    def get_queryset(self):
        return (
            super(RationaleOnlyManager, self).get_queryset().filter(type="RO")
        )


class RationaleOnlyQuestion(Question):
    objects = RationaleOnlyManager()

    class Meta:
        proxy = True

    def start_form_valid(request, view, form):
        rationale = form.cleaned_data["rationale"]

        # Set first_answer_choice to 0 to indicate null
        answer = Answer(
            question=view.question,
            assignment=view.assignment,
            first_answer_choice=0,
            rationale=rationale,
            user_token=view.user_token,
            time=timezone.now(),
        )
        answer.save()

        view.emit_event(
            "save_problem_success",
            success="correct",
            rationale=rationale,
            grade=answer.get_grade(),
        )
        view.stage_data.clear()

        return

    def is_correct(*args):
        return True

    def get_start_form_class(self):
        from ..forms import RationaleOnlyForm

        return RationaleOnlyForm
