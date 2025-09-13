from django import forms
from django.contrib.auth.forms import UserCreationForm

from usersapp.models import User


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'phone')










