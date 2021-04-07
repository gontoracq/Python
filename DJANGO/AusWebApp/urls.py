# -*- coding: utf-8 -*-
from django.urls import path, url

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    url(r'^home/$', views.main, name='main')
]
