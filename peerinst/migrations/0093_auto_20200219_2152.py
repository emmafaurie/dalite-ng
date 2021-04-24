# Generated by Django 2.2.9 on 2020-02-19 21:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0002_auto_20200219_2139"),
        ("peerinst", "0092_auto_20190902_0345"),
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
            name="StudentGroupCourse",
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
                ("added_on", models.DateTimeField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Course",
                    ),
                ),
                (
                    "student_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="peerinst.StudentGroup",
                    ),
                ),
            ],
            options={
                "verbose_name": "Group-Course Link",
                "verbose_name_plural": "Group-Course Links",
            },
        ),
    ]
