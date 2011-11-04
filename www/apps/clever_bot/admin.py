# -*- coding: utf-8 -*-

from django.contrib import admin
from clever_bot.models import MentionKeyword, Status, DefaultAnswer



admin.site.register(MentionKeyword)
admin.site.register(Status)
admin.site.register(DefaultAnswer)

