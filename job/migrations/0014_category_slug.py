# Generated by Django 4.1 on 2022-10-28 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0013_job_favourite'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
