# Generated by Django 4.0.2 on 2022-03-03 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='careers',
            name='job_qualification',
            field=models.TextField(default='BCA'),
            preserve_default=False,
        ),
    ]