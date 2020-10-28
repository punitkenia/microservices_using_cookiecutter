from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.db import models

# Create your models here.
class RouterDetails(models.Model):
    class Meta:
        db_table = 'router_details'

    sapid = models.CharField(max_length=100, null=False,)
    hostname = models.CharField(max_length=100, null=False, blank=False)
    loopback = models.CharField(max_length=100, null=False)
    mac_address = models.CharField(max_length=100, null=False, blank=False)
    is_deleted = models.BooleanField(default=False)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
