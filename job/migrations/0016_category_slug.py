# Generated by Django 4.1 on 2022-10-28 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0015_remove_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=None, null=True, unique=True),
        ),
    ]
