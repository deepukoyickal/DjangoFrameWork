# Generated by Django 4.0.2 on 2022-03-01 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(default='null', max_length=20)),
                ('date', models.CharField(max_length=30)),
                ('time', models.CharField(max_length=20)),
                ('purpose', models.TextField()),
                ('fixed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BoardMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(upload_to='board_members/')),
                ('name', models.CharField(max_length=255)),
                ('designation1', models.CharField(max_length=255)),
                ('designation2', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Careers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('job_description', models.TextField()),
                ('job_pdf', models.FileField(upload_to='careers/')),
                ('date', models.DateField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=255)),
                ('organizers', models.TextField()),
                ('event_content', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.CharField(max_length=255)),
                ('more_info', models.FileField(upload_to='events/')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FileField(upload_to='gallery/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('pdf', models.FileField(upload_to='news/')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('user', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OurTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('fb_link', models.CharField(default='null', max_length=255)),
                ('twitter_link', models.CharField(default='null', max_length=255)),
                ('insta_link', models.CharField(default='null', max_length=255)),
                ('linkedin_link', models.CharField(default='null', max_length=255)),
                ('profile_pic', models.FileField(upload_to='our_team/')),
            ],
        ),
        migrations.CreateModel(
            name='QueriesAndReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
