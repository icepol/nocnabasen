from django.contrib.auth.models import User
from django.db import models


class Basen(models.Model):
    vers = models.CharField('Vers', max_length=255)
    inserted = models.DateTimeField('Inserted', auto_now_add=True)
    user = models.ForeignKey(User)
    ip = models.IPAddressField('Author IP')
    user_agent = models.CharField('User agent', max_length=255)
    enabled = models.IntegerField('Enabled', default=1)