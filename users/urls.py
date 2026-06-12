from django.urls import path

from .views import (EmailSentView, EmailVerifyView, UserBlockView,
                    UserListView, UserLoginView, UserRegisterView, logout_view)

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("verify/<str:token>/", EmailVerifyView.as_view(), name="verify"),
    path("email-sent/", EmailSentView.as_view(), name="email_sent"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/block/", UserBlockView.as_view(), name="user_block"),
]
