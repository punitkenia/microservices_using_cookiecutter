from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from simple_history.models import HistoricalRecords
from simple_history import register

from django.db import models

# Create your models here.
register(User)
register(Token)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserInfo(models.Model):
    class Meta:
        db_table = 'user_info'

    email_verify = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    history = HistoricalRecords()
