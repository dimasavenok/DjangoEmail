from django.contrib.auth import views as auth_views
from django.urls import path

from usersapp.views import RegisterView, ActivateView, ProfileView

app_name = "usersapp"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "signup/done/",
        auth_views.TemplateView.as_view(template_name="usersapp/register_done.html"),
        name="register_done",
    ),
    path("activate/<uidb64>/<token>", ActivateView.as_view(), name="activate"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="usersapp/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
