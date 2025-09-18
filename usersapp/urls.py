

from django.contrib.auth import views
from django.urls import path

from usersapp.views import RegisterView, ActivateView

app_name = 'usersapp'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),

    path('login/', views.LoginView.as_view(template_name='usersapp/login.html'), name='login'),
]