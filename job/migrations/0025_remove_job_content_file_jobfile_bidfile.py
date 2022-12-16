# Generated by Django 4.1 on 2022-12-15 15:37

from django.db import migrations, models
import django.db.models.deletion
import job.validators


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0024_job_content_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='content_file',
        ),
        migrations.CreateModel(
            name='JobFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, help_text='Allowed size is 50MB', upload_to='job_files', validators=[job.validators.validate_file_size], verbose_name='Job Files')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
            ],
        ),
        migrations.CreateModel(
            name='BidFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, help_text='Allowed size is 50MB', upload_to='bid_files', validators=[job.validators.validate_file_size], verbose_name='Bid Files')),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.bid')),
            ],
        ),
    ]
