# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import upload
from .views import renew

urlpatterns = [
    url(r'^$', upload, name='list'),
    url(r'^upload/$', upload, name='list'),
    url(r'^renew/$', renew, name='renew')
]
