from __future__ import unicode_literals
import mptt
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
# Create your models here.


class Message(MPTTModel):
    user = models.ForeignKey(User)
    message = models.CharField('message', max_length=255)
    date_save = models.DateTimeField()
    likes = models.IntegerField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['-date_save']

    def __unicode__(self):
        return self.message
mptt.register(Message,)
