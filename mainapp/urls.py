from django.urls import path

from mainapp.views import MailingHomeView, RecipientListView, RecipientCreateView, RecipientUpdateView, \
    RecipientDeleteView

app_name = 'mainapp'

urlpatterns = [
    path('', MailingHomeView.as_view(), name='home'),

    path('recipients/', RecipientListView.as_view(), name='recipients_list'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipients/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),

]