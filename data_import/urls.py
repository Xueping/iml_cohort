# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import list
from .views import renew

urlpatterns = [
    url(r'^list/$', list, name='list'),
    url(r'^renew/$', renew, name='renew')
]
