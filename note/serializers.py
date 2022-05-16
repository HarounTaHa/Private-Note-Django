from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class NoteFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['note_name', 'note', 'is_destroy']
