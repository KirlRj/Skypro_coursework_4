from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       UserCreationForm)

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["email", "password"]


class UserPasswordResetForm(PasswordResetForm):
    pass
