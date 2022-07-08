# Generated by Django 1.11.18 on 2019-02-19 16:22


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("peerinst", "0065_auto_20190219_0512"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeacherNotification",
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
                ("object_id", models.PositiveIntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "notification_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="peerinst.Teacher",
                    ),
                ),
            ],
        ),
        migrations.AlterModelOptions(
            name="lastlogout", options={"get_latest_by": ["last_logout"]}
        ),
        migrations.AlterField(
            model_name="lastlogout",
            name="last_logout",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
