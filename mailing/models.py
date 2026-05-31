from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=200, verbose_name="Ф.И.О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    topic = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(blank=False, null=False, verbose_name="Письмо")

    def __str__(self):
        return f"{self.topic}"

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"


class Mailing(models.Model):
    start_time = models.DateTimeField(
        blank=False, null=False, verbose_name="Начало отправки рассылки"
    )
    end_time = models.DateTimeField(
        blank=False, null=False, verbose_name="Конец отправки рассылки"
    )
    status = models.CharField(max_length=20, default="Создана", verbose_name="Cтатус")
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Письмо"
    )
    recipients = models.ManyToManyField(Client, verbose_name="Получатели")

    def update_status(self):
        from django.utils import timezone

        now = timezone.now()
        if now < self.start_time:
            new_status = "Создана"
        elif self.start_time <= now <= self.end_time:
            new_status = "Запущена"
        else:
            new_status = "Завершена"

        if self.status != new_status:
            self.status = new_status
            self.save()

    def __str__(self):
        return f"Рассылка {self.start_time}-{self.end_time}. Статус {self.status}."

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class MailingAttempt(models.Model):
    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    status = models.CharField(max_length=20, verbose_name="Статус рассылки")
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ почтового сервера"
    )
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )

    def __str__(self):
        return f"Попытка рассылки от {self.attempt_time} - {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
