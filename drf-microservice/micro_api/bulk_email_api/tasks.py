from celery import shared_task
from django.core.mail import send_mail
from time import sleep
import logging

logger = logging.getLogger('django')

@shared_task(bind=True)
def send_email_task(self, body, subject, from_email, to_email):
    # sleep(10)

    try:
        for email in to_email:
            send_mail(subject, body, from_email, [email]) # List of emails
    except Exception as ex:
        logger.exception("send_email_task[Celery] raised an exception: " + str(ex))

    return 'Mail sent successfuly'