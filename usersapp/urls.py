from django.contrib.auth import views
from django.urls import path

from usersapp.views import RegisterView

app_name = 'usersapp'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', views.LoginView.as_view(), name='login'),
]