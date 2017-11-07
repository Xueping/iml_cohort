# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import visual
from .views import explore
from .views import compare

urlpatterns = [
    url(r'^visual/$', visual, name='visual'),
    url(r'^explore/$', explore, name='explore'),
    url(r'^compare/$', compare, name='compare'),
]
