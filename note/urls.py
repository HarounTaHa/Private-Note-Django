from django.urls import path

from note.views import create_note, check_note, fetch_note

app_name = 'note'

urlpatterns = [
    path('create/', create_note, name='create'),
    path('<str:note_id>/', fetch_note, name='get-note-without-password'),
    path('fetch/<str:note_id>', check_note, name='get-note-with-password'),

]
