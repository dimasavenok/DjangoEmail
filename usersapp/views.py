from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from usersapp.forms import UserRegisterForm


# Create your views here.
class RegisterView(CreateView):
    template_name = 'usersapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('mainapp:home')

