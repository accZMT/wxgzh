# -*- coding: utf-8 -*-
# python 3.6
"""
-------------------------------------------------
   File Name：     urls
   Description :
   Author :       17971
   date：          2018/10/22
-------------------------------------------------
   Change Activity:
                   2018/10/22
-------------------------------------------------
"""

from django.urls import path
from wechat.views import handle_wx, create_menu, add_material, add_permanent_material


app_name = 'wx'
urlpatterns = [
    path('', handle_wx),
    path('create_menu/', create_menu),
    path('add_material/', add_material, name='add_material'),
    path('add_permanent_material/', add_permanent_material, name='add_permanent_material'),
]
