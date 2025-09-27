from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.cache import cache
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
)

from mainapp.forms import RecipientForm, MessageForm, MailingForm
from mainapp.models import Recipient, Message, Mailing, MailingAttempt
from mainapp.services import send_mailing_sync


# Create your views here.
class OwnerOrManagerMixin:
    owner_field = "owner"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return qs
        model = qs.model
        if (
            user.has_perm(f"{model._meta.app_label}.view_all_{model._meta.model_name}s")
            or user.groups.filter(name="Managers").exists()
        ):
            return qs
        return qs.filter(**{self.owner_field: user})


class MailingHomeView(TemplateView):
    template_name = "mainapp/index.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return super().get_context_data(**kwargs)
        cache_key = f"user_stats_{user.pk}"
        data = cache.get(cache_key)
        if not data:
            total_mailings = Mailing.objects.filter(owner=user).count()
            active_mailings = Mailing.objects.filter(
                owner=user, status=Mailing.STATUS_RUNNING
            ).count()
            unique_recipients = Recipient.objects.filter(owner=user).count()
            # статистика попыток:
            success_count = MailingAttempt.objects.filter(
                mailing__owner=user, status=MailingAttempt.STATUS_SUCCESS
            ).count()
            failed_count = MailingAttempt.objects.filter(
                mailing__owner=user, status=MailingAttempt.STATUS_FAILED
            ).count()
            data = {
                "total_mailings": total_mailings,
                "active_mailings": active_mailings,
                "unique_recipients": unique_recipients,
                "success_count": success_count,
                "failed_count": failed_count,
            }
            cache.set(cache_key, data, 60)
        ctx = super().get_context_data(**kwargs)
        ctx.update(data)
        return ctx


# Recipients
class RecipientListView(LoginRequiredMixin, OwnerOrManagerMixin, ListView):
    model = Recipient
    template_name = "mainapp/recipients_list.html"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mainapp/recipient_form.html"
    success_url = reverse_lazy("mainapp:recipients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mainapp/recipient_form.html"
    success_url = reverse_lazy("mainapp:recipients_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name="Managers").exists():
            qs = qs.filter(owner=self.request.user)
        return qs


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mainapp/confirm_delete.html"
    success_url = reverse_lazy("mainapp:recipients_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name="Managers").exists():
            qs = qs.filter(owner=self.request.user)
        return qs


# messages
class MessageListView(LoginRequiredMixin, OwnerOrManagerMixin, ListView):
    model = Message
    template_name = "mainapp/messages_list.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mainapp/message_form.html"
    success_url = reverse_lazy("mainapp:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerOrManagerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mainapp/message_form.html"
    success_url = reverse_lazy("mainapp:messages_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mainapp/confirm_delete.html"
    success_url = reverse_lazy("mainapp:messages_list")

    def get_queryset(self):
        qs = super().get_queryset()
        # if not self.request.user.groups.filter(name="Managers").exists():
        #     qs = qs.filter(owner=self.request.user)
        return qs


# mailing
class MailingListView(LoginRequiredMixin, OwnerOrManagerMixin, ListView):
    model = Mailing
    template_name = "mainapp/mailings_list.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mainapp/mailing_form.html"
    success_url = reverse_lazy("mainapp:mailings_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mainapp/mailing_detail.html"


class MailingDeleteView(LoginRequiredMixin, OwnerOrManagerMixin,  DeleteView):
    model = Mailing
    template_name = "mainapp/confirm_delete.html"
    success_url = reverse_lazy("mainapp:mailings_list")


# send
class SendMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        # проверка прав
        if (
            mailing.owner != request.user
            and not request.user.groups.filter(name="Managers").exists()
        ):
            return render(request, "403.html", status=403)
        # выполнить отправку синхронно (или запустить таск)
        send_mailing_sync(mailing_id=mailing.pk)
        messages.success(request, "Запущено отправление рассылки.")
        # очистить кеш отчётов
        cache.delete(f"user_stats_{request.user.pk}")
        return redirect("mainapp:mailings_list")
