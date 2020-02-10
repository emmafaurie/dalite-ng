# Generated by Django 2.2.9 on 2020-02-10 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('peerinst', '0093_auto_20200210_1709'), ('peerinst', '0094_remove_usertype_colour')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('peerinst', '0092_auto_20190902_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='collaborators',
            field=models.ManyToManyField(blank=True, help_text='Optional. Other users that may also edit this question.', limit_choices_to=models.Q(teacher__isnull=False), related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='url', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewUserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peerinst.UserType')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
