from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^upload', views.upload_file, name='upload_file'),
    url(r'^$', views.clusteringMethod, name="clusteringMethod"),
    url(r'^clustering', views.clusteringMethod, name="clusteringMethod")

]
