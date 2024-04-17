# Generated by Django 5.0.4 on 2024-04-16 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solverrapp', '0005_remove_question_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='display_body',
            field=models.TextField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='display_image',
            field=models.TextField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='display_text',
            field=models.TextField(blank=True, max_length=3000, null=True),
        ),
    ]
