# -*- coding: utf-8 -*-

from django.db import models
from account.models import User


class MentionKeyword(models.Model):
    keyword = models.CharField(max_length=32, default=None)
    
    class Meta:
        verbose_name = u'palavra-chave das menções'
        verbose_name_plural = u'palavras-chave das menções'

    def __unicode__(self):
        return self.keyword

class Status(models.Model):
    twitter_account = models.ForeignKey(User, 
            verbose_name=u'usuário', related_name='twitter_account')
    text = models.CharField(max_length=140, default=None)
    keyword = models.ManyToManyField(MentionKeyword, blank=True)

    def __unicode__(self):
        return self.text

class Settings(models.Model):
    twitter_account = models.ForeignKey(User, 
            verbose_name=u'settings', related_name='twitter_settings')
    last_id = models.CharField(max_length=100, default=None)
