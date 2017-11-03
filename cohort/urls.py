'''
Created on 3 Nov 2017

@author: xuepeng
'''

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload', views.upload_file, name='upload_file'),
]

