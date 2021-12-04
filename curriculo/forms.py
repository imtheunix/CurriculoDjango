from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = {"username", "email", "descricao_user",
                  "profilepic", "comentario", }
        field_classes = {"username": UsernameField}
