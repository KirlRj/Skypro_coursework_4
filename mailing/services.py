from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import MailingAttempt
from django.core.cache import cache

def send_mailing(mailing):
    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        return 'Рассылка не активна в данный момент.'

    attempts = []

    for client in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.topic,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[client.email],
            )
            attempts.append(MailingAttempt(
                status='Успешно',
                mailing=mailing,
            ))
        except Exception as e:
            attempts.append(MailingAttempt(
                status='Не успешно',
                server_response=str(e),
                mailing=mailing,
            ))

    MailingAttempt.objects.bulk_create(attempts)

    if mailing.owner:
        cache.delete(f'home_stats_{mailing.owner.id}')

    return 'Рассылка выполнена.'
