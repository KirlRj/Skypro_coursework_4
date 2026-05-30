from django.urls import path
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = 'mailing'

urlpatterns = [
    path('', ClientListView.as_view(), name='clients'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
]