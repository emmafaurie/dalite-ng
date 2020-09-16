# Generated by Django 2.2.14 on 2020-07-31 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peerinst', '0099_auto_20200731_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='conclusion_page',
            field=models.TextField(blank=True, help_text='Any notes you would like to leave for students to read that will be shown after the last question of the assignment.', null=True, verbose_name='Post Assignment Notes'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='intro_page',
            field=models.TextField(blank=True, help_text='Any special instructions you would like students to read before they start the assignment.', null=True, verbose_name='Assignment Cover Page'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.TextField(blank=True, help_text='Notes you would like keep for yourself (or other teachers) regarding this assignment', null=True, verbose_name='Description'),
        ),
    ]
