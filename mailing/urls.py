from django.urls import path
from django.views.generic import RedirectView

from mailing.views import (ClientCreateView, ClientDeleteView,
                           ClientDetailView, ClientListView, ClientUpdateView,
                           MailingCreateView, MailingDeleteView,
                           MailingDetailView, MailingListView,
                           MailingUpdateView, MessageCreateView,
                           MessageDeleteView, MessageDetailView,
                           MessageListView, MessageUpdateView)

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
    path('mailing/', MailingListView.as_view(), name='mailings'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
]