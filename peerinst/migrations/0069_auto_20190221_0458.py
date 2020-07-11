# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-21 04:58


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("peerinst", "0068_merge_20190220_1704")]

    operations = [
        migrations.AlterField(
            model_name="answerannotation",
            name="score",
            field=models.PositiveIntegerField(
                blank=True,
                choices=[
                    (1, "1-Never Show"),
                    (2, "2-Maybe Show"),
                    (3, "3-Show"),
                ],
                default=None,
                null=True,
            ),
        )
    ]
