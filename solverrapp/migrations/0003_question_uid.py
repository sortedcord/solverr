# Generated by Django 5.0.4 on 2024-04-16 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solverrapp', '0002_question_question_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='uid',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
