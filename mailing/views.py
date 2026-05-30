from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client

class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'client_detail.html'
    context_object_name = 'client'

class ClientCreateView(CreateView):
    model = Client
    template_name = 'client_create.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создать клиента"
        return context

class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'client_update.html'
    fields = ['email', 'full_name', 'comment']

    def get_success_url(self):
        return reverse_lazy('mailing:client_detail', kwargs={'pk': self.object.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать клиента"
        return context

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('mailing:clients')
