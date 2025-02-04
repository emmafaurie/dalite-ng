# Generated by Django 2.2.20 on 2021-04-24 23:51

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import peerinst.models.group
import peerinst.models.question


class Migration(migrations.Migration):

    dependencies = [
        ("peerinst", "0092_auto_20190902_0345"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="collaborators",
            field=models.ManyToManyField(
                blank=True,
                help_text="Optional. Other users that may also edit this question.",
                limit_choices_to=models.Q(teacher__isnull=False),
                related_name="collaborators",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Enter the name of a new subject.",
                        max_length=100,
                        unique=True,
                        validators=[peerinst.models.question.no_hyphens],
                        verbose_name="Subject name",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="subjects",
                        to="peerinst.Category",
                    ),
                ),
                (
                    "discipline",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="peerinst.Discipline",
                    ),
                ),
            ],
            options={
                "verbose_name": "subject",
                "verbose_name_plural": "subjects",
            },
        ),
        migrations.CreateModel(
            name="UserUrl",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.TextField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="url",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NewUserRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="peerinst.UserType",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="assignmentquestions",
            name="rank",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name="assignmentquestions",
            options={"ordering": ("rank",)},
        ),
        migrations.AddField(
            model_name="assignment",
            name="created_on",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="assignment",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Notes you would like keep for yourself\n            (or other teachers) regarding this assignment\n            ",
                null=True,
                verbose_name="Description",
            ),
        ),
        migrations.AddField(
            model_name="assignment",
            name="last_modified",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name="assignment",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="peerinst.Assignment",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="video_url",
            field=models.URLField(
                blank=True,
                help_text="Optional. A video or simulation to include after the question text. All videos should include transcripts.  Only videos from youtube (i.e. https://www.youtube.com/embed/...) and simulations from phet (i.e. https://phet.colorado.edu/sims/html/...) are currently supported.",
                verbose_name="Question video URL",
            ),
        ),
        migrations.AddField(
            model_name="assignment",
            name="intro_page",
            field=models.TextField(
                blank=True,
                help_text="Any special instructions you would like\n            students to read before they start the assignment.\n            ",
                null=True,
                verbose_name="Assignment Cover Page",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="answerannotation",
            unique_together={("answer", "annotator")},
        ),
        migrations.AddField(
            model_name="studentgroup",
            name="discipline",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="peerinst.Discipline",
            ),
        ),
        migrations.AddField(
            model_name="assignment",
            name="conclusion_page",
            field=models.TextField(
                blank=True,
                help_text="Any notes you would like to leave for students\n            to read that will be shown after the last\n            question of the assignment.\n            ",
                null=True,
                verbose_name="Post Assignment Notes",
            ),
        ),
        migrations.AlterField(
            model_name="answerannotation",
            name="note",
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="studentgroup",
            name="semester",
            field=models.CharField(
                choices=[
                    ("FALL", "Fall"),
                    ("SUMMER", "Summer"),
                    ("WINTER", "Winter"),
                ],
                default=peerinst.models.group.current_semester,
                max_length=6,
            ),
        ),
        migrations.AddField(
            model_name="studentgroup",
            name="year",
            field=models.PositiveIntegerField(
                default=peerinst.models.group.current_year,
                validators=[
                    django.core.validators.MinValueValidator(2015),
                    peerinst.models.group.max_value_current_year,
                ],
            ),
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="blinkassignment",
                    name="blinkquestions",
                ),
                migrations.RemoveField(
                    model_name="blinkassignment",
                    name="teacher",
                ),
                migrations.RemoveField(
                    model_name="blinkassignmentquestion",
                    name="blinkassignment",
                ),
                migrations.RemoveField(
                    model_name="blinkassignmentquestion",
                    name="blinkquestion",
                ),
                migrations.RemoveField(
                    model_name="blinkquestion",
                    name="question",
                ),
                migrations.RemoveField(
                    model_name="blinkquestion",
                    name="teacher",
                ),
                migrations.RemoveField(
                    model_name="blinkround",
                    name="question",
                ),
            ],
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.AlterModelTable(
                    name="BlinkAnswer",
                    table="blink_blinkanswer",
                ),
                migrations.AlterModelTable(
                    name="BlinkAssignment",
                    table="blink_blinkassignment",
                ),
                migrations.AlterModelTable(
                    name="BlinkAssignmentQuestion",
                    table="blink_blinkassignmentquestion",
                ),
                migrations.AlterModelTable(
                    name="BlinkQuestion",
                    table="blink_blinkquestion",
                ),
                migrations.AlterModelTable(
                    name="BlinkRound",
                    table="blink_blinkround",
                ),
            ],
            state_operations=[
                migrations.DeleteModel(
                    name="BlinkAnswer",
                ),
                migrations.DeleteModel(
                    name="BlinkAssignment",
                ),
                migrations.DeleteModel(
                    name="BlinkAssignmentQuestion",
                ),
                migrations.DeleteModel(
                    name="BlinkQuestion",
                ),
                migrations.DeleteModel(
                    name="BlinkRound",
                ),
            ],
        ),
    ]
