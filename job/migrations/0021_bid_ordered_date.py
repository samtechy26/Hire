# Generated by Django 4.1 on 2022-12-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0020_remove_job_job_category_job_job_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='ordered_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
