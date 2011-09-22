from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Category(models.Model):
    category = models.CharField('Category', max_length = 10)
    color = models.CharField('Color', max_length = 6)

    def __unicode__(self):
        return self.category

class Topic(models.Model):
    TOPIC_TYPE = (
        (1, 'Text'),
        (2, 'Foto')
    )
    topic_type =  models.IntegerField('Topic type', choices = TOPIC_TYPE)
    topic = models.CharField('Topic text', max_length = 255)
    inserted = models.DateTimeField('Inserted', default = datetime.now())
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    ip = models.IPAddressField('Author IP')
    user_agent = models.CharField('User agent', max_length = 255)
    enabled = models.IntegerField('Enabled', default = 1)

    def __unicode__(self):
        return self.topic

class Comment(models.Model):
    topic = models.ForeignKey(Topic)
    comment = models.CharField('Comment text', max_length = 200)
    inserted = models.DateTimeField('Insertd', default = datetime.now())
    user = models.ForeignKey(User)
    ip = models.IPAddressField('Author IP')
    user_agent = models.CharField('User agent', max_length = 255)
    enabled = models.IntegerField('Enabled', default = 1) 

    def __unicode__(self):
        return self.comment

class Photo(models.Model):
    topic = models.ForeignKey(Topic)
    photo = models.ImageField(upload_to = 'photos/')
