# Generated by Django 4.1.3 on 2022-12-03 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='subject',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
