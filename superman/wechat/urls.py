#coding: utf-8

from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.wechat, name='wechat'),
    url(r'test', views.test),

]
