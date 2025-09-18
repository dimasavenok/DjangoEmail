from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView

from usersapp.forms import UserRegisterForm
from usersapp.models import User


# Create your views here.
class RegisterView(CreateView):
    template_name = 'usersapp/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('mainapp:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse_lazy('usersapp:activate', kwargs={'uidb64': uid, 'token': token})
        )
        print(activation_link)
        return super().form_valid(form)


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None
        print(user, '------------------------', default_token_generator.check_token(user, token))
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('mainapp:home')
        return render(request, "usersapp/activate_invalid.html")
