from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=320, null=True, blank=True)
    profilepic = models.ImageField(null=True, blank=True)
    backgroundpic = models.ImageField(null=True)
    descricao_user = models.TextField(max_length=250, null=True, blank=True)
    comentario = models.TextField(max_length=500, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    pass