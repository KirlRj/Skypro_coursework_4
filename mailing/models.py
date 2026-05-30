from django.db import models

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=200, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'