# Generated by Django 2.2.28 on 2022-07-28 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peerinst', '0108_auto_20210814_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentgroup',
            name='mode_created',
            field=models.CharField(choices=[('LTI', 'LTI'), ('STANDALONE', 'STANDALONE'), ('LTI_STANDAONE', 'LTI_STANDALONE')], default='STANDALONE', max_length=20),
        ),
    ]
