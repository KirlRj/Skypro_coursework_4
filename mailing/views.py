from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import MailingForm
from .models import Client, Mailing, Message
from .services import send_mailing


class ClientListView(ListView):
    model = Client
    template_name = "client_list.html"
    context_object_name = "clients"


class ClientDetailView(DetailView):
    model = Client
    template_name = "client_detail.html"
    context_object_name = "client"


class ClientCreateView(CreateView):
    model = Client
    template_name = "client_create.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailing:clients")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать клиента"
        return context


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "client_update.html"
    fields = ["email", "full_name", "comment"]

    def get_success_url(self):
        return reverse_lazy("mailing:client_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать клиента"
        return context


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client_delete.html"
    success_url = reverse_lazy("mailing:clients")


class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MessageCreateView(CreateView):
    model = Message
    template_name = "message_create.html"
    fields = ["topic", "body"]
    success_url = reverse_lazy("mailing:messages")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать сообщение"
        return context


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "message_update.html"
    fields = ["topic", "body"]

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать сообщение"
        return context


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_delete.html"
    success_url = reverse_lazy("mailing:messages")


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing_create.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать рассылку"
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = "mailing_update.html"
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать рассылку"
        return context


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing_delete.html"
    success_url = reverse_lazy("mailing:mailings")


def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    result = send_mailing(mailing)
    messages.success(request, result)
    return redirect("mailing:mailing_detail", pk=pk)
