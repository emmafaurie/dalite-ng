# Generated by Django 1.11.20 on 2019-04-03 16:40


from django.db import migrations, models

import dalite.models.custom_fields


class Migration(migrations.Migration):

    dependencies = [("quality", "0003_auto_20190327_1407")]

    operations = [
        migrations.CreateModel(
            name="RightAnswerCriterion",
            fields=[
                (
                    "version",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "uses_rules",
                    dalite.models.custom_fields.CommaSepField(
                        blank=True,
                        help_text="Comma separated list of used rules for the criterion found as the fields of the associated rules object. Make sure to use the verbose_name",  # noqa
                    ),
                ),
                ("is_beta", models.BooleanField(default=False)),
                ("binary_threshold", models.BooleanField(default=False)),
                (
                    "name",
                    models.CharField(
                        default="right_answer", editable=False, max_length=32
                    ),
                ),
                (
                    "for_quality_types",
                    models.ManyToManyField(to="quality.QualityType"),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="RightAnswerCriterionRules",
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
                    "threshold",
                    dalite.models.custom_fields.ProbabilityField(
                        help_text="Minimum value for the answer to be accepted",  # noqa
                        verbose_name="Threshold",
                    ),
                ),
                (
                    "only_last",
                    models.BooleanField(
                        help_text="Only the second step (or first if no second step) is evaluated. If false, both steps are evaluated.",  # noqa
                        verbose_name="Only last step evaluated",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]
