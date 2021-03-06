"""cheng URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from express.views import data_import
from express.views import change_follower
from express.auth_login import auth_login


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^import/$', data_import),
    url(r'^change/$', change_follower, name='all'),
    url(r'^change/(?P<username>\w{3,20})$', change_follower, name="change"),
    url(r'^accounts/login/$', auth_login),
]
