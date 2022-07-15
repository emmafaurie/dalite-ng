# Generated by Django 1.11.18 on 2019-03-10 02:51


import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("peerinst", "0073_question_second_answer_needed_correct")]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="identifier",
            field=models.CharField(
                help_text="A unique identifier for this assignment used for inclusion in a course.  Only use letters, numbers and/or the underscore for the identifier.",  # noqa
                max_length=100,
                primary_key=True,
                serialize=False,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.",  # noqa
                        "invalid",
                    )
                ],
                verbose_name="identifier",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ManyToManyField(
                help_text="Select at least one category for this question. You can select multiple categories.",  # noqa
                related_name="Categories",
                to="peerinst.Category",
            ),
        ),
    ]
