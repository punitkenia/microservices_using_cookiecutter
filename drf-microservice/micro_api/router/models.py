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

