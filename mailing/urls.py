from django.urls import path
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MessageDetailView
from django.views.generic import RedirectView
app_name = 'mailing'

urlpatterns = [
    path('', RedirectView.as_view(url='/clients/'), name='home'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
]