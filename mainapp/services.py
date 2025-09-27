from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mainapp.models import Mailing, MailingAttempt


def send_mailing_sync(mailing_id):
    mailing = (
        Mailing.objects.select_related("message")
        .prefetch_related("recipients")
        .get(pk=mailing_id)
    )
    message = mailing.message
    recipients = mailing.recipients.all()
    first_send = True  # not mailing.attempts.exists()

    if first_send:
        mailing.status = Mailing.STATUS_RUNNING
        mailing.save(update_fields=["status"])

    for r in recipients:
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[r.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=r,
                status=MailingAttempt.STATUS_SUCCESS,
                response_server="OK",
            )
        except Exception as exc:
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=r,
                status=MailingAttempt.STATUS_FAILED,
                response_server=str(exc),
            )
    # после выполнения — если текущее время > end_at — пометить как finished
    if timezone.now() > mailing.end_at:
        mailing.status = Mailing.STATUS_FINISHED
        mailing.save(update_fields=["status"])
