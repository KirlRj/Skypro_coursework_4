from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import MailingForm
from .models import Client, Mailing, MailingAttempt, Message
from .services import send_mailing
from django.core.cache import cache

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Client
    template_name = "client_detail.html"
    context_object_name = "client"

    def test_func(self):
        return (
            self.get_object().owner == self.request.user
            or self.request.user.groups.filter(name="Менеджер").exists()
        )


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = "client_create.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailing:clients")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать клиента"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    template_name = "client_update.html"
    fields = ["email", "full_name", "comment"]

    def test_func(self):
        return self.get_object().owner == self.request.user

    def get_success_url(self):
        return reverse_lazy("mailing:client_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать клиента"
        return context


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = "client_delete.html"
    success_url = reverse_lazy("mailing:clients")

    def test_func(self):
        return self.get_object().owner == self.request.user


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"

    def test_func(self):
        obj = self.get_object()
        return (
            obj.owner == self.request.user
            or self.request.user.groups.filter(name="Менеджер").exists()
        )


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "message_create.html"
    fields = ["topic", "body"]
    success_url = reverse_lazy("mailing:messages")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать сообщение"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    template_name = "message_update.html"
    fields = ["topic", "body"]

    def test_func(self):
        return self.get_object().owner == self.request.user

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать сообщение"
        return context


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = "message_delete.html"
    success_url = reverse_lazy("mailing:messages")

    def test_func(self):
        return self.get_object().owner == self.request.user


@method_decorator(cache_page(60), name="dispatch")
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Менеджер").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"

    def test_func(self):
        obj = self.get_object()
        return (
            obj.owner == self.request.user
            or self.request.user.groups.filter(name="Менеджер").exists()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(
            name="Менеджер"
        ).exists()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    template_name = "mailing_create.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать рассылку"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    template_name = "mailing_update.html"
    form_class = MailingForm

    def test_func(self):
        return self.get_object().owner == self.request.user

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать рассылку"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = "mailing_delete.html"
    success_url = reverse_lazy("mailing:mailings")

    def test_func(self):
        return self.get_object().owner == self.request.user

@login_required
@require_POST
def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    result = send_mailing(mailing)
    messages.success(request, result)
    return redirect("mailing:mailing_detail", pk=pk)


@method_decorator(cache_page(60), name="dispatch")
class HomeView(TemplateView):
    template_name = 'home.html'

    @method_decorator(cache_control(max_age=60, public=True), name='dispatch')
    class HomeView(TemplateView):
        template_name = 'home.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            user = self.request.user
            cache_key = f'home_stats_{user.id if user.is_authenticated else "anon"}'

            stats = cache.get(cache_key)
            if stats is None:
                now = timezone.now()
                for mailing in Mailing.objects.all():
                    mailing.update_status()

                mailings_qs = Mailing.objects.all()
                attempts_qs = MailingAttempt.objects.all()

                if user.is_authenticated and not user.groups.filter(name='Менеджер').exists():
                    mailings_qs = mailings_qs.filter(owner=user)
                    attempts_qs = attempts_qs.filter(mailing__owner=user)

                stats = {
                    'all_mailing': mailings_qs.count(),
                    'active_mailings': mailings_qs.filter(
                        status='Запущена',
                        start_time__lte=now,
                        end_time__gte=now,
                    ).count(),
                    'total_clients': Client.objects.count(),
                    'successful_attempts': attempts_qs.filter(status='Успешно').count(),
                    'failed_attempts': attempts_qs.filter(status='Не успешно').count(),
                    'total_attempts': attempts_qs.count(),
                }
                cache.set(cache_key, stats, timeout=60)

            context.update(stats)
            return context

class OwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner == self.request.user

    def handle_no_permission(self):
        return redirect("mailing:home")
