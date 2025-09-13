from django.urls import path

from mainapp.views import MailingHomeView

app_name = 'mainapp'

urlpatterns = [
    path('', MailingHomeView.as_view(), name='home'),
]