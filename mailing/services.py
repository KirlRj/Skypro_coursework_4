from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import MailingAttempt


def send_mailing(mailing):
    """Отправка почты"""

    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        return "Рассылка не активна в данный момент."

    for client in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.topic,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[client.email],
            )
            MailingAttempt.objects.create(
                status="Успешно",
                mailing=mailing,
            )
        except Exception as e:
            MailingAttempt.objects.create(
                status="Не успешно",
                server_response=str(e),
                mailing=mailing,
            )

    return "Рассылка выполнена."
