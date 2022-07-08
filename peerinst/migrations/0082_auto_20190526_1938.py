# Generated by Django 1.11.18 on 2019-05-26 19:38


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("peerinst", "0081_collection_featured"),
    ]

    operations = [
        migrations.CreateModel(
            name="MetaFeature",
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
                ("key", models.CharField(max_length=20)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("S", "String"),
                            ("F", "Float"),
                            ("I", "Integer"),
                        ],
                        default="S",
                        max_length=2,
                    ),
                ),
                ("value", models.CharField(max_length=256)),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="MetaSearch",
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
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "meta_feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="peerinst.MetaFeature",
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="metafeature", unique_together={("key", "type", "value")}
        ),
    ]
