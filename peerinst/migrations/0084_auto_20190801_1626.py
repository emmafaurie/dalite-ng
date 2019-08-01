# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-01 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("peerinst", "0083_merge_20190610_1742")]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="filtered_with_quality",
            field=models.ForeignKey(
                blank=True,
                help_text="Which quality was used to filter shown rationales.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="filtering_quality",
                to="quality.Quality",
            ),
        )
    ]
