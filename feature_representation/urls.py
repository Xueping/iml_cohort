#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^upload', views.upload_file, name='upload_file'),
    url(r'^$', views.features_representation, name="features_index"),
    url(r'^features', views.features_representation, name="features")

]
