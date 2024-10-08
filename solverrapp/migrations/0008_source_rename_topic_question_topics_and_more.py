# Generated by Django 5.0.4 on 2024-04-17 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solverrapp', '0007_alter_question_question_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('source_type', models.CharField(choices=[('PYQ', 'Previous Year'), ('ASN', 'Assignment'), ('MOD', 'Coaching Module'), ('TSR', 'Test Series'), ('BOOK', 'Book'), ('MISC', 'Miscellaneous')], max_length=300)),
            ],
        ),
        migrations.RenameField(
            model_name='question',
            old_name='topic',
            new_name='topics',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_author',
        ),
        migrations.RemoveField(
            model_name='question',
            name='source',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subject',
        ),
        migrations.AddField(
            model_name='question',
            name='sources',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='solverrapp.source'),
        ),
    ]
