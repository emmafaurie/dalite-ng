# Generated by Django 1.11.20 on 2019-02-17 03:59


import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("peerinst", "0063_auto_20190123_1523"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnswerAnnotation",
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
                ("timestamp", models.DateTimeField(auto_now=True)),
                (
                    "score",
                    models.PositiveIntegerField(
                        blank=True,
                        choices=[
                            (1, "1-Very Weak"),
                            (2, "2-Weak"),
                            (3, "3-Neutral"),
                            (4, "4-Strong"),
                            (5, "5-Very Strong"),
                        ],
                        default=None,
                        null=True,
                    ),
                ),
                (
                    "note",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "annotator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="peerinst.Answer",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ManyToManyField(
                blank=True,
                help_text="""Optional. Select categories for this question.
                You can select multiple categories.""",
                related_name="Categories",
                to="peerinst.Category",
            ),
        ),
    ]
