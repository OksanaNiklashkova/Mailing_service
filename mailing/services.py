from .views import Mailing, SendAttempt
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.timezone import localtime
from config.settings import EMAIL_HOST_USER

def send_message(pk, request=None):
    """Отправка рассылки по требованию"""
    mailing = Mailing.objects.get(pk=pk)
    now = timezone.now()

    if request and mailing.owner != request.user:
        SendAttempt.objects.create(
            mailing=mailing,
            status=SendAttempt.STATUS_UNSUCCES,
            server_response=f'Рассылку пытался отправить посторонний человек: {request.user.email}',
            attempt_datetime=now,
        )
        return False

    topik = mailing.message.topik
    message=mailing.message.text
    recipient_list = [recipient.email for recipient in mailing.recipients.all()]

    if mailing.status == Mailing.STATUS_FINISHED:
        SendAttempt.objects.create(
            mailing=mailing,
            status=SendAttempt.STATUS_UNSUCCES,
            server_response='Рассылка уже завершена',
            attempt_datetime=now,
            owner=request.user,
        )
        return False

    elif now < mailing.started_at:
        SendAttempt.objects.create(
            mailing=mailing,
            status=SendAttempt.STATUS_UNSUCCES,
            server_response=f'Время рассылки еще не наступило (начало - {mailing.started_at}, сейчас - {now})',
            attempt_datetime=now,
            owner=request.user,
        )
        return False

    elif now > mailing.finished_at:
        mailing.status = Mailing.STATUS_FINISHED
        mailing.save()
        SendAttempt.objects.create(
            mailing=mailing,
            status=SendAttempt.STATUS_UNSUCCES,
            server_response=f'Время рассылки уже прошло (конец - {mailing.finished_at}, сейчас - {now})',
            attempt_datetime=now,
            owner=request.user,
        )
        return False

    if not recipient_list:
        SendAttempt.objects.create(
            mailing=mailing,
            status=SendAttempt.STATUS_UNSUCCES,
            server_response='Нет получателей рассылки',
            attempt_datetime=now,
            owner=request.user,
        )
        return False

    try:
        send_mail(
            subject=topik,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        SendAttempt.objects.create(
            mailing=mailing,
            status=SendAttempt.STATUS_SUCCESS,
            server_response='Рассылка отправлена',
            attempt_datetime=now,
            owner=request.user
        )
        if mailing.status == Mailing.STATUS_CREATED:
            mailing.status = Mailing.STATUS_STARTED
            mailing.save()

        return True

    except Exception as ex:
        SendAttempt.objects.create(
            mailing=mailing,
            status=SendAttempt.STATUS_UNSUCCES,
            server_response=str(ex),
            attempt_datetime=now,
        )
        return False