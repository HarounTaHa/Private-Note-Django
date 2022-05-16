from django.contrib import admin
from .models import Note


# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ['note', 'note_id', 'created_at']


admin.site.register(Note, NoteAdmin)
