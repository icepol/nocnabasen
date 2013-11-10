"""
Registration models.
"""
from hashlib import md5
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Invitation(models.Model):
    sender = models.ForeignKey(get_user_model())
    email = models.EmailField()
    code = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.code = md5('{}{}{}'.format(self.email, settings.SECRET_KEY, datetime.now())).hexdigest()

        super(Invitation, self).save(force_insert, force_update, using, update_fields)