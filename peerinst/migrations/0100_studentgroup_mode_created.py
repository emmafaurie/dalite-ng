# Generated by Django 2.2.24 on 2021-07-18 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peerinst', '0099_studentgroup_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgroup',
            name='mode_created',
            field=models.CharField(choices=[('LTI', 'LTI'), ('STANDALONE', 'STANDALONE')], default='STANDALONE', max_length=10),
        ),
    ]
