# Generated by Django 4.1 on 2022-09-28 11:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0012_denom_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='favourite',
            field=models.ManyToManyField(blank=True, related_name='fav_task', to=settings.AUTH_USER_MODEL),
        ),
    ]
