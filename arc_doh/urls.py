"""arc_doh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cohort/', include('cohort.urls')),
#     url(r'^policy/', include('policy.urls')),
    url(r'^clustering/', include('clustering.urls')),
    url(r'^data_import/', include('data_import.urls')),
    url(r'^represent/', include('feature_representation.urls')),
#     url(r'^metric/', include('metric.urls')),
    url(r'^visualization/', include('visualization.urls')),
    
]
