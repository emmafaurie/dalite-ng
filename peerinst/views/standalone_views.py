# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_safe
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from tos.models import Tos

from ..forms import EmailForm, StudentGroupAssignmentForm
from ..mixins import LoginRequiredMixin, NoStudentsMixin
from ..models import (
    Assignment,
    Question,
    Student,
    StudentAssignment,
    StudentGroup,
    StudentGroupAssignment,
    Teacher,
)
from ..students import authenticate_student


def signup_through_link(request, group_hash):

    # Call logout to ensure a clean session
    logout(request)

    group = StudentGroup.get(group_hash)

    if group is None:
        return TemplateResponse(
            request,
            "404.html",
            context={
                "message": _(
                    "The group couldn't be found. Bear in mind that the URL "
                    "is case-sensitive."
                )
            },
            stauts=404,
        )

    if request.method == "POST":

        form = EmailForm(request.POST)
        if not form.is_valid():
            return TemplateResponse(
                request,
                "400.html",
                context={
                    "message": _("There was a problem with the values sent.")
                },
                status=400,
            )

        student, created = Student.get_or_create(form.cleaned_data["email"])

        if student is None:
            return TemplateResponse(
                request,
                "400.html",
                context={
                    "message": _(
                        "There already exists a user with this "
                        "username. Try a different email address."
                    )
                },
                status=400,
            )

        if created:
            student.join_group(group, mail_type="confirmation")
        else:
            student.join_group(group, mail_type="new_group")

        return TemplateResponse(
            request,
            "registration/sign_up_student_done.html",
            context={"student": student, "group": group},
        )

    form = EmailForm()
    tos = Tos.objects.filter(role="student").latest("created").text

    return TemplateResponse(
        request,
        "registration/sign_up_student.html",
        context={"form": form, "group": group, "tos": tos},
    )


@require_safe
def live(request, token, assignment_hash):

    # Call logout to ensure a clean session
    logout(request)

    # Login through token
    user = authenticate_student(request, token)
    if isinstance(user, HttpResponse):
        return user
    login(request, user)

    # Register access type
    request.session["LTI"] = False

    # Get assignment for this token and current question
    group_assignment = StudentGroupAssignment.get(assignment_hash)
    student_assignment = StudentAssignment.objects.get(
        student=user.student, group_assignment=group_assignment
    )

    # Register assignment
    request.session["assignment"] = assignment_hash

    assignment = student_assignment.group_assignment
    current_question = student_assignment.get_current_question()
    has_expired = student_assignment.group_assignment.expired

    if has_expired or current_question is None:
        return HttpResponseRedirect(reverse("finish-assignment"))

    questions = assignment.questions
    idx = questions.index(current_question)

    request.session["assignment_first"] = idx == 0
    request.session["assignment_last"] = idx == len(questions) - 1
    request.session["assignment_expired"] = has_expired

    # Redirect to view
    return HttpResponseRedirect(
        reverse(
            "question",
            kwargs={
                "assignment_id": assignment.assignment.pk,
                "question_id": current_question.id,
            },
        )
    )


@login_required
@require_safe
def navigate_assignment(request, assignment_id, question_id, direction, index):

    hash = request.session.get("assignment")
    if hash is None:

        if not Teacher.objects.filter(user=request.user).exists():
            return TemplateResponse(
                request,
                "400.html",
                context={
                    "message": _(
                        "Try logging in again using the link to this "
                        "assignment sent via email."
                    )
                },
                status=400,
            )

        assignment = get_object_or_404(Assignment, pk=assignment_id)
        questions = list(assignment.questions.all())
        current_question = get_object_or_404(Question, pk=question_id)
        idx = questions.index(current_question)
        if direction == "next":
            if idx < len(questions) - 1:
                new_question = questions[idx + 1]
            else:
                new_question = questions[0]
        else:
            if idx > 0:
                new_question = questions[idx - 1]
            else:
                new_question = questions[-1]

        # Redirect
        return HttpResponseRedirect(
            reverse(
                "question",
                kwargs={
                    "assignment_id": assignment.pk,
                    "question_id": new_question.id,
                },
            )
        )

    else:

        assignment = StudentGroupAssignment.get(hash)
        question = get_object_or_404(Question, id=question_id)

        if index != "x":
            idx = int(index)
        else:
            idx = None

        new_question = assignment.get_question(
            current_question=question, after=direction == "next", idx=idx
        )

        if new_question is None:
            return HttpResponseRedirect(reverse("student-page"))

        questions = assignment.questions
        idx = questions.index(new_question)

        request.session["assignment_first"] = idx == 0
        request.session["assignment_last"] = idx == len(questions) - 1

        if not request.session["assignment_expired"] and assignment.expired:
            request.session["assignment_expired"] = assignment.expired
            return HttpResponseRedirect(reverse("finish-assignment"))

    # Redirect
    return HttpResponseRedirect(
        reverse(
            "question",
            kwargs={
                "assignment_id": assignment.assignment.pk,
                "question_id": new_question.id,
            },
        )
    )


@login_required
@require_safe
@require_http_methods(["GET"])
def finish_assignment(req):
    hash_ = req.session["assignment"]
    assignment = StudentGroupAssignment.get(hash_)
    req.session["assignment_first"] = True
    req.session["assignment_last"] = len(assignment.questions) == 1
    req.session["assignment_expired"] = True

    try:
        student_assignment = StudentAssignment.objects.get(
            student__student=req.user, group_assignment=assignment
        )
        has_expired = assignment.expired and not student_assignment.completed
    except Student.DoesNotExist:
        has_expired = assignment.expired

    context = {
        "assignment_id": assignment.assignment.pk,
        "question_id": assignment.questions[0].id,
        "has_expired": has_expired,
    }
    return render(req, "peerinst/student/assignment_complete.html", context)


class StudentGroupAssignmentCreateView(
    LoginRequiredMixin, NoStudentsMixin, CreateView
):
    """View to distribute an assignment to a group."""

    model = StudentGroupAssignment
    form_class = StudentGroupAssignmentForm

    def get_form(self):
        form = super(StudentGroupAssignmentCreateView, self).get_form()
        teacher = get_object_or_404(Teacher, user=self.request.user)
        form.fields["group"].queryset = teacher.current_groups.all()

        return form

    def form_valid(self, form):
        # Attach assignment and save
        form.instance.assignment = get_object_or_404(
            Assignment, pk=self.kwargs["assignment_id"]
        )
        self.object = form.save()

        self.object.update_students()

        return super(StudentGroupAssignmentCreateView, self).form_valid(form)

    def get_success_url(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        return reverse("group-assignments", kwargs={"teacher_id": teacher.pk})

    def get_context_data(self, **kwargs):
        context = super(
            StudentGroupAssignmentCreateView, self
        ).get_context_data(**kwargs)
        teacher = get_object_or_404(Teacher, user=self.request.user)
        context["assignment"] = get_object_or_404(
            Assignment, pk=self.kwargs["assignment_id"]
        )
        context["teacher"] = teacher
        return context


class StudentGroupAssignmentListView(
    LoginRequiredMixin, NoStudentsMixin, ListView
):
    model = StudentGroupAssignment
    template_name = "peerinst/teacher/studentgroup_assignments.html"

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        queryset = StudentGroupAssignment.objects.filter(
            group__teacher=teacher
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentGroupAssignmentListView, self).get_context_data(
            **kwargs
        )
        teacher = get_object_or_404(Teacher, user=self.request.user)
        context["teacher"] = teacher
        return context
