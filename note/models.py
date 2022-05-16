import datetime

from django.db import models
import uuid

# Create your models here.
from django.utils import timezone

from core import settings


class Note(models.Model):
    choices_self_destructs = [
        (datetime.timedelta(), "after reading it"),
        (datetime.timedelta(hours=1), "1 hour from now"),
        (datetime.timedelta(hours=24), "24 hour from now"),
        (datetime.timedelta(days=7), "7 days from now"),
        (datetime.timedelta(days=30), "30 days from now"),
    ]
    note_id = models.CharField(max_length=8, unique=True, primary_key=True, blank=True, editable=False)
    note = models.TextField()
    key = models.CharField(max_length=250, blank=True)
    email = models.EmailField(help_text='E-mail to notify when note is destroyed', blank=True)
    password = models.CharField(help_text='Enter a custom password to encrypt the note', max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    duration_self_destroy = models.DurationField(blank=True, null=True, default=choices_self_destructs[0][0]
                                                 , choices=choices_self_destructs)
    note_name = models.CharField(help_text='Reference name for the note (optional)', max_length=100, blank=True)
    is_destroy = models.BooleanField(default=False)
    question_showing = models.BooleanField(help_text='ask for confirmation before showing and destroying the note',
                                           default=False)
    link_note = models.URLField(max_length=200, blank=True)
    is_showing = models.BooleanField(default=False)

    def save(
            self, *args, **kwargs
    ):
        if not self.note_id:
            self.note_id = uuid.uuid4().hex[:8]
            if self.password:
                self.link_note = f'http://127.0.0.1:8000/note/fetch/{self.note_id}'
            else:
                self.link_note = f'http://127.0.0.1:8000/note/{self.note_id}'

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.note
