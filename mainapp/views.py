from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView

from mainapp.forms import RecipientForm
from mainapp.models import Recipient


# Create your views here.
class OwnerOrManagerMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        return qs.filter(**{'owner': user})


class MailingHomeView(TemplateView):
    template_name = 'mainapp/index.html'


# Recipients
class RecipientListView(LoginRequiredMixin, OwnerOrManagerMixin, ListView):
    model = Recipient
    template_name = 'mainapp/recipients_list.html'


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mainapp/recipient_form.html'
    success_url = reverse_lazy('mainapp:recipients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mainapp/recipient_form.html'
    success_url = reverse_lazy('mainapp:recipients_list')

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='Managers').exists():
            qs = qs.filter(owner=self.request.user)
        return qs

class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = 'mainapp/confirm_delete.html'
    success_url = reverse_lazy('mainapp:recipients_list')

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='Managers').exists():
            qs = qs.filter(owner=self.request.user)
        return qs