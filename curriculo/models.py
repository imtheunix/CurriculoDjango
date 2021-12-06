from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    email = models.EmailField(max_length=320, null=True, blank=True)
    profilepic = models.ImageField(null=True, blank=True)
    backgroundpic = models.ImageField(null=True)
    descricao_user = models.TextField(max_length=250, null=True, blank=True)
    comentario = models.TextField(max_length=500, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    pass

class Room(models.Model):
    name = models.CharField(max_length=50)

class Message(models.Model):
    value = models.CharField(max_length=255, blank=False, null=False, error_messages={'required': 'Por favor, escreva algo'})
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=50)
    room = models.CharField(max_length=50)

class MyDateTimeFeild(models.DateTimeField):
    def get_prep_value(self, value):
        from dateutil.parser import parse
        from datetime import timedelta
        td = float(value[-5:])/100
        timediff = timedelta(hours=td)
        return parse(value).replace(tzinfo=None) - timediff