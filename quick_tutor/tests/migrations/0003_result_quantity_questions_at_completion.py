# Generated by Django 5.0.6 on 2024-07-10 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_result_is_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='quantity_questions_at_completion',
            field=models.PositiveIntegerField(default=0),
        ),
    ]