# -*- coding:utf-8 -*-

from django.urls import path
from api.views import get_hour_num

urlpatterns = [
    path('get_hour_num',get_hour_num)
]
