import secrets

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView

from .forms import UserLoginForm, UserRegisterForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("users:email_sent")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        verify_url = f"http://127.0.0.1:8000/users/verify/{token}/"
        send_mail(
            subject="Подтверждение email",
            message=f"Перейдите по ссылке для подтверждения: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return redirect("users:email_sent")


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "login.html"


class EmailVerifyView(TemplateView):
    def get(self, request, token):
        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.email_verified = True
        user.token = None
        user.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("mailing:home")


class EmailSentView(TemplateView):
    template_name = "email_sent.html"


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"

    def test_func(self):
        return self.request.user.groups.filter(name="Менеджер").exists()


class UserBlockView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Менеджер").exists()

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_superuser:
            return redirect("users:user_list")
        user.is_active = not user.is_active
        user.save()
        return redirect("users:user_list")


def logout_view(request):
    logout(request)
    return redirect("users:login")
