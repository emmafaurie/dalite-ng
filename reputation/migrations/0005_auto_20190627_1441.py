# Generated by Django 1.11.21 on 2019-06-27 14:41


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("reputation", "0004_auto_20190625_1852")]

    operations = [
        migrations.AddField(
            model_name="nanswerscriterion",
            name="badge_colour",
            field=models.CharField(default="#0066ff", max_length=16),
        ),
        migrations.AddField(
            model_name="nquestionscriterion",
            name="badge_colour",
            field=models.CharField(default="#0066ff", max_length=16),
        ),
    ]
