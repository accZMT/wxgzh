# -*- coding: utf-8 -*-
# python 3.6
"""
-------------------------------------------------
   File Name：     settings_example
   Description :
-------------------------------------------------
"""

ALLOWED_HOSTS = ["*"]

# 以下为微信公共号中的测试号信息
APP_ID = 'wx76342d45a73b2237'
APP_SECRET = '5d7402129992ff3710be8f772198a068'

# 腾讯AI开放平台个人密钥
app_id = '2109258854'
app_key = 'LSFaIB44cBW7dOKB'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 添加新建的app
    'wechat.apps.WechatConfig',
]
