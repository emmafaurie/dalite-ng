# Generated by Django 1.11.22 on 2019-08-27 01:53


import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("peerinst", "0089_auto_20190821_1842")]

    operations = [
        migrations.AddField(
            model_name="message",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        )
    ]
