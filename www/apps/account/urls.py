# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('account.views',
    url(r'^email/$', 'email', name='account_email'),
)