# Generated by Django 5.0.4 on 2024-04-17 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solverrapp', '0009_remove_question_sources_question_sources'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='topics',
        ),
    ]
