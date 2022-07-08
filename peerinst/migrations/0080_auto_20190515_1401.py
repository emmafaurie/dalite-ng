# Generated by Django 1.11.20 on 2019-05-15 14:01


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reputation", "0002_nquestionscriterion"),
        ("peerinst", "0079_merge_20190410_1221"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="reputation",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="reputation.Reputation",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="reputation",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="reputation.Reputation",
            ),
        ),
        migrations.AddField(
            model_name="teacher",
            name="reputation",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="reputation.Reputation",
            ),
        ),
        migrations.AlterField(
            model_name="studentgroupassignment",
            name="order",
            field=models.TextField(blank=True),
        ),
    ]
