# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import visual
from .views import explore
from .views import compare
import views

urlpatterns = [
    url(r'^visual/$', visual, name='visual'),
    url(r'^explore/$', explore, name='explore'),
    url(r'^compare/$', compare, name='compare'),
    url(r'^labeling/$', views.labeling, name='labeling'),
]
