# Generated by Django 4.0.4 on 2022-05-16 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('note_id', models.CharField(blank=True, editable=False, max_length=8, primary_key=True, serialize=False, unique=True)),
                ('note', models.TextField()),
                ('key', models.CharField(blank=True, max_length=250)),
                ('email', models.EmailField(blank=True, help_text='E-mail to notify when note is destroyed', max_length=254)),
                ('password', models.CharField(blank=True, help_text='Enter a custom password to encrypt the note', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('duration_self_destroy', models.DurationField(blank=True, choices=[(datetime.timedelta(0), 'after reading it'), (datetime.timedelta(seconds=3600), '1 hour from now'), (datetime.timedelta(days=1), '24 hour from now'), (datetime.timedelta(days=7), '7 days from now'), (datetime.timedelta(days=30), '30 days from now')], default=datetime.timedelta(0), null=True)),
                ('note_name', models.CharField(blank=True, help_text='Reference name for the note (optional)', max_length=100)),
                ('is_destroy', models.BooleanField(default=False)),
                ('question_showing', models.BooleanField(default=False, help_text='ask for confirmation before showing and destroying the note')),
                ('link_note', models.URLField(blank=True)),
                ('is_showing', models.BooleanField(default=False)),
            ],
        ),
    ]