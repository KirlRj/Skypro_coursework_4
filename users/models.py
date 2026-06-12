from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    email_verified = models.BooleanField(
        default=False, verbose_name="Email подтверждён"
    )
    token = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Токен"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
