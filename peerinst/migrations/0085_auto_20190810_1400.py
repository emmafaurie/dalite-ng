# Generated by Django 1.11.23 on 2019-08-10 14:00


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reputation", "0006_merge_20190807_1816"),
        ("peerinst", "0084_auto_20190716_1930"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="reputation",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="reputation.Reputation",
            ),
        )
    ]
