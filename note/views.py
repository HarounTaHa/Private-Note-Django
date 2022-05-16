import binascii
import datetime
import hashlib
import os
import secrets
import base64

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from rest_framework import serializers, status
from rest_framework.decorators import api_view

from core import settings
from .models import Note
from .serializers import NoteSerializer, NoteFetchSerializer
from rest_framework.response import Response

from .utility._2way_encryption_aes import AESCipher


@api_view(['POST'])
def create_note(request):
    raw_data = {}
    email_field = ''
    note_name_field = ''
    password_field = ''
    note_field = ''
    # -----------Get Data----------
    note = request.data.get('note', None)
    password = request.data.get('password', None)
    email = request.data.get('email', None)
    note_name = request.data.get('name', None)
    # --------------Implement----------------
    key = secrets.token_hex(32)
    if note:
        note_field = AESCipher(key).encrypt(note).decode()
        if password:
            password2 = request.data.get('password2', None)
            if password2 is None:
                raise serializers.ValidationError({"message": 'you must add field confirm password'})
            if password == password2:
                # password encryption process
                salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
                password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                                    salt, 100000)
                pwdhash = binascii.hexlify(password_hash)
                # password encrypted stored in variable
                password_field = (salt + pwdhash).decode('ascii')
            else:
                raise serializers.ValidationError({"message": 'field password1 in not equal field password2'})

        if email:
            email_field = email

        if note_name:
            note_name_field = note_name

        # insert raw data in dictionary
        raw_data.update({'note': note_field})
        raw_data.update({'key': key})
        raw_data.update({'email': email_field})
        raw_data.update({'password': password_field})
        raw_data.update({'note_name': note_name_field})

        # validate raw data using serializer
        note_serializer = NoteSerializer(data=raw_data)
        if note_serializer.is_valid():
            note_serializer.save()
            send_mail(f'{note_name_field}', f'This Link to show note : {note_serializer.data["link_note"] }', settings.EMAIL_HOST,
                      ['harountaha@outlook.sa'])
            return Response({'data': note_serializer.data})
        else:
            return Response({'Error': note_serializer.errors})
    else:
        return Response({"message": 'Error: the note field text is empty.'}, status=status.HTTP_400_BAD_REQUEST)


# Request Fetch Note Without Password
@api_view(['GET'])
def fetch_note(request, note_id):
    try:
        note = Note.objects.get(note_id=note_id)
    except Exception:
        raise serializers.ValidationError({"message": 'Note ID is not existing'})

    if note.password:
        return JsonResponse(
            {
                'Message': 'The note need password to get note you must send request POST on the url below with note_id and password field',
                'URL': 'http://127.0.0.1:8000/note/fetch/'})
    if not note.is_destroy:
        duration_destroy = note.duration_self_destroy
        date_time_created = note.created_at.replace(tzinfo=None) + datetime.timedelta(hours=3)
        date_time_now = datetime.datetime.now()
        result_difference_date_time = date_time_now - date_time_created
        if duration_destroy < result_difference_date_time and not duration_destroy == datetime.timedelta():
            note.is_destroy = True
            note.save()
        if not note.is_destroy and not note.is_showing:
            if duration_destroy == datetime.timedelta():
                note.is_showing = True
                note.is_destroy = True
                note.save()
            note.note = AESCipher(note.key).decrypt(note.note)
            serializer = NoteFetchSerializer(note)
            return Response(serializer.data)
        else:
            raise serializers.ValidationError({"message": 'The message is destroy'})

    else:
        raise serializers.ValidationError({"message": 'The message is destroy'})


# Request Fetch Note With Password
@api_view(['POST'])
def check_note(request, note_id):
    password = request.data.get('password', None)
    if note_id:
        try:
            note = Note.objects.get(note_id=note_id)
        except:
            raise serializers.ValidationError({"message": 'Note ID is not existing'})
        if password:
            password_hash = note.password
            salt = password_hash[:64]
            stored_password = password_hash[64:]
            password_input = password
            pwdhash = hashlib.pbkdf2_hmac('sha512',
                                          password_input.encode('utf-8'),
                                          salt.encode('ascii'),
                                          100000)
            pwdhash = binascii.hexlify(pwdhash).decode('ascii')
            if pwdhash == stored_password:
                if not note.is_destroy:
                    duration_destroy = note.duration_self_destroy
                    date_time_created = note.created_at.replace(tzinfo=None) + datetime.timedelta(hours=3)
                    date_time_now = datetime.datetime.now()
                    result_difference_date_time = date_time_now - date_time_created

                    if duration_destroy < result_difference_date_time and not duration_destroy == datetime.timedelta():
                        note.is_destroy = True
                        note.save()
                    if not note.is_destroy and not note.is_showing:
                        if duration_destroy == datetime.timedelta():
                            note.is_showing = True
                            note.is_destroy = True
                            note.save()
                        note.note = AESCipher(note.key).decrypt(note.note)
                        serializer = NoteFetchSerializer(note)

                        return Response(serializer.data)
                    else:
                        raise serializers.ValidationError({"message": 'The message is destroy'})

                else:
                    raise serializers.ValidationError({"message": 'The message is destroy'})
            else:
                raise serializers.ValidationError({"message": 'Password incorrect. Please enter it again'})
        else:
            raise serializers.ValidationError({"message": 'Field password required'})
    else:
        raise serializers.ValidationError({"message": 'Field note_id required'})
