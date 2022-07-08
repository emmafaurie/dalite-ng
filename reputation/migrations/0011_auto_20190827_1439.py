# Generated by Django 1.11.22 on 2019-08-27 14:39


from django.db import migrations

import dalite.models.custom_fields


class Migration(migrations.Migration):

    dependencies = [
        ('reputation', '0010_merge_20190827_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonrationalechoicescriterion',
            name='points_per_threshold',
            field=dalite.models.custom_fields.CommaSepField(default='[1]', help_text='Number of reputation points for each criterion point up to the next threadhold, split by commas. This list should have the same length or have one more element than Thresholds.', verbose_name='Points per threshold'),
        ),
        migrations.AlterField(
            model_name='convincingrationalescriterion',
            name='points_per_threshold',
            field=dalite.models.custom_fields.CommaSepField(default='[1]', help_text='Number of reputation points for each criterion point up to the next threadhold, split by commas. This list should have the same length or have one more element than Thresholds.', verbose_name='Points per threshold'),
        ),
        migrations.AlterField(
            model_name='nanswerscriterion',
            name='points_per_threshold',
            field=dalite.models.custom_fields.CommaSepField(default='[1]', help_text='Number of reputation points for each criterion point up to the next threadhold, split by commas. This list should have the same length or have one more element than Thresholds.', verbose_name='Points per threshold'),
        ),
        migrations.AlterField(
            model_name='nquestionscriterion',
            name='points_per_threshold',
            field=dalite.models.custom_fields.CommaSepField(default='[1]', help_text='Number of reputation points for each criterion point up to the next threadhold, split by commas. This list should have the same length or have one more element than Thresholds.', verbose_name='Points per threshold'),
        ),
        migrations.AlterField(
            model_name='questionlikedcriterion',
            name='points_per_threshold',
            field=dalite.models.custom_fields.CommaSepField(default='[1]', help_text='Number of reputation points for each criterion point up to the next threadhold, split by commas. This list should have the same length or have one more element than Thresholds.', verbose_name='Points per threshold'),
        ),
        migrations.AlterField(
            model_name='rationaleevaluationcriterion',
            name='points_per_threshold',
            field=dalite.models.custom_fields.CommaSepField(default='[1]', help_text='Number of reputation points for each criterion point up to the next threadhold, split by commas. This list should have the same length or have one more element than Thresholds.', verbose_name='Points per threshold'),
        ),
        migrations.AlterField(
            model_name='studentrationaleevaluationcriterion',
            name='points_per_threshold',
            field=dalite.models.custom_fields.CommaSepField(default='[1]', help_text='Number of reputation points for each criterion point up to the next threadhold, split by commas. This list should have the same length or have one more element than Thresholds.', verbose_name='Points per threshold'),
        ),
    ]
