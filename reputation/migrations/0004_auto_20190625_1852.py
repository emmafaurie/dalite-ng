# Generated by Django 1.11.21 on 2019-06-25 18:52


from django.db import migrations

import dalite.models.custom_fields
import reputation.models.criteria.criterion


class Migration(migrations.Migration):

    dependencies = [("reputation", "0003_auto_20190522_1817")]

    operations = [
        migrations.AddField(
            model_name="nanswerscriterion",
            name="badge_thresholds",
            field=dalite.models.custom_fields.CommaSepField(
                blank=True,
                help_text="Thresholds for the badges to be awarded.",
                validators=[
                    reputation.models.criteria.criterion.validate_list_floats_greater_0
                ],
            ),
        ),
        migrations.AddField(
            model_name="nquestionscriterion",
            name="badge_thresholds",
            field=dalite.models.custom_fields.CommaSepField(
                blank=True,
                help_text="Thresholds for the badges to be awarded.",
                validators=[
                    reputation.models.criteria.criterion.validate_list_floats_greater_0
                ],
            ),
        ),
    ]
