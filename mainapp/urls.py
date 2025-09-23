from django.urls import path

from mainapp.views import (
    MailingHomeView,
    RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView,
    MessageListView, MessageCreateView,
    MailingListView, MailingCreateView, MailingDetailView,
    SendMailingView, MessageUpdateView
)

app_name = 'mainapp'

urlpatterns = [
    path('', MailingHomeView.as_view(), name='home'),

    path('recipients/', RecipientListView.as_view(), name='recipients_list'),
    path('recipients/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipients/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),

    path('mailings/', MailingListView.as_view(), name='mailings_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/send/', SendMailingView.as_view(), name='mailing_send'),
]
