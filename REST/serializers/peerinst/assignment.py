import bleach
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import bad_request

from peerinst.models import (
    Assignment,
    AssignmentQuestions,
    Category,
    Discipline,
    Question,
)
from peerinst.templatetags.bleach_html import ALLOWED_TAGS

from .dynamic_serializer import DynamicFieldsModelSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title"]

    def to_representation(self, instance):
        """Bleach"""
        ret = super().to_representation(instance)
        ret["title"] = bleach.clean(
            ret["title"], tags=[], styles=[], strip=True
        ).strip()
        return ret


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["title", "pk"]

    def to_representation(self, instance):
        """Bleach"""
        ret = super().to_representation(instance)
        ret["title"] = bleach.clean(
            ret["title"], tags=[], styles=[], strip=True
        ).strip()
        return ret


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class QuestionSerializer(DynamicFieldsModelSerializer):
    answer_count = serializers.ReadOnlyField()
    answerchoice_set = serializers.SerializerMethodField()
    assignment_count = serializers.ReadOnlyField()
    category = CategorySerializer(many=True, read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    difficulty = serializers.SerializerMethodField()
    discipline = DisciplineSerializer(read_only=True)
    frequency = serializers.SerializerMethodField()
    matrix = serializers.SerializerMethodField()
    most_convincing_rationales = serializers.SerializerMethodField()
    peer_impact = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    def get_answer_count(self, obj):
        return obj.answer_count

    def get_assignment_count(self, obj):
        return obj.assignment_count

    def get_answerchoice_set(self, obj):
        return [
            {
                "correct": obj.is_correct(i),
                "text": bleach.clean(
                    ac[1],
                    tags=ALLOWED_TAGS,
                    styles=[],
                    strip=True,
                ).strip(),
            }
            for i, ac in enumerate(obj.get_choices(), 1)
        ]

    def get_difficulty(self, obj):
        d = obj.get_difficulty()
        return {"score": d[0], "label": str(d[1])}

    def get_frequency(self, obj):
        return obj.get_frequency()

    def get_matrix(self, obj):
        return obj.get_matrix()

    def get_most_convincing_rationales(self, obj):
        return obj.get_most_convincing_rationales()

    def get_peer_impact(self, obj):
        pi = obj.get_peer_impact()
        return {"score": pi[0], "label": str(pi[1])}

    class Meta:
        model = Question
        fields = [
            "answer_count",
            "answerchoice_set",
            "answer_style",
            "assignment_count",
            "category",
            "collaborators",
            "difficulty",
            "discipline",
            "frequency",
            "image",
            "image_alt_text",
            "matrix",
            "most_convincing_rationales",
            "peer_impact",
            "pk",
            "text",
            "title",
            "type",
            "user",
            "video_url",
        ]

    def to_representation(self, instance):
        """Bleach HTML-supported fields"""
        ret = super().to_representation(instance)
        if "title" in ret:
            ret["title"] = bleach.clean(
                ret["title"], tags=ALLOWED_TAGS, styles=[], strip=True
            ).strip()
        if "text" in ret:
            ret["text"] = bleach.clean(
                ret["text"], tags=ALLOWED_TAGS, styles=[], strip=True
            ).strip()
        return ret


class RankSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(
        read_only=True,
        fields=(
            "answer_count",
            "answerchoice_set",
            "category",
            "collaborators",
            "discipline",
            "frequency",
            "image",
            "image_alt_text",
            "matrix",
            "pk",
            "text",
            "title",
            "user",
        ),
    )

    def create(self, validated_data):
        """Custom create method to add questions to an assignment based on pk
        Required POST data:
            - assignment (validated normally)
            - question_pk (validated here)
        """

        assignment = validated_data["assignment"]
        if (
            assignment.editable
            and self.context["request"].user in assignment.owner.all()
        ):
            if "question_pk" in self.context["request"].data:
                question_pk = self.context["request"].data["question_pk"]
                if assignment.questions.all():
                    added_question = AssignmentQuestions.objects.create(
                        assignment=assignment,
                        question=get_object_or_404(Question, pk=question_pk),
                        rank=assignment.questions.aggregate(
                            Max("assignmentquestions__rank")
                        )["assignmentquestions__rank__max"]
                        + 1,
                    )
                else:
                    added_question = AssignmentQuestions.objects.create(
                        assignment=assignment,
                        question=get_object_or_404(Question, pk=question_pk),
                        rank=1,
                    )
                if added_question:
                    return added_question
                else:
                    raise bad_request
            else:
                raise bad_request
        raise PermissionDenied

    class Meta:
        model = AssignmentQuestions
        fields = ["assignment", "question", "rank", "pk"]


class AssignmentSerializer(DynamicFieldsModelSerializer):
    editable = serializers.SerializerMethodField()
    questions = RankSerializer(
        source="assignmentquestions_set",
        many=True,
        required=False,
    )
    question_pks = serializers.SerializerMethodField()
    urls = serializers.SerializerMethodField()

    def get_editable(self, obj):
        return obj.editable

    def get_question_pks(self, obj):
        return list(obj.questions.values_list("pk", flat=True))

    def get_urls(self, obj):
        return {
            "distribute": reverse(
                "student-group-assignment-create", args=(obj.pk,)
            ),
            "preview": obj.get_absolute_url(),
            "update": reverse("assignment-update", args=(obj.pk,)),
        }

    def validate_questions(self, data):
        assignment_questions = list(
            self.instance.assignmentquestions_set.all()
        )
        if len(data) == len(assignment_questions):
            return data
        else:
            raise serializers.ValidationError(
                "Question list must contain all questions from this assignment"
            )

    def create(self, validated_data):
        """Attach user and add to teacher assignments"""
        assignment = super().create(validated_data)
        assignment.owner.add(self.context["request"].user)
        self.context["request"].user.teacher.assignments.add(assignment)
        return assignment

    def update(self, instance, validated_data):
        """
        Only used to reorder questions.
        Adding/deleting questions is handled by serializer for through table.
        """
        if instance.editable:
            for i, aq in enumerate(instance.assignmentquestions_set.all()):
                aq.rank = validated_data["assignmentquestions_set"][i]["rank"]
                aq.save()

            return instance
        raise PermissionDenied

    def to_representation(self, instance):
        """Bleach fields"""
        ret = super().to_representation(instance)
        for field in ["conclusion_page", "description", "intro_page"]:
            if field in ret and ret[field]:
                ret[field] = bleach.clean(
                    ret[field], tags=ALLOWED_TAGS, styles=[], strip=True
                ).strip()
        for field in ["title"]:
            if field in ret and ret[field]:
                ret[field] = bleach.clean(
                    ret[field], tags=[], styles=[], strip=True
                ).strip()
        return ret

    class Meta:
        model = Assignment
        fields = [
            "conclusion_page",
            "description",
            "editable",
            "intro_page",
            "pk",
            "question_pks",
            "questions",
            "title",
            "urls",
        ]
