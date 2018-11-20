# -*- coding: utf-8 -*-
# python 3.6
"""
-------------------------------------------------
   File Name：     news
   Description :
   Author :       17971
   date：          2018/10/24
-------------------------------------------------
   Change Activity:
                   2018/10/24
-------------------------------------------------
"""

import requests


def get_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = "http://c.3g.163.com/nc/article/list/T1467284926140/0-10.html"
    response = requests.get(url, headers=headers)

    return response.json()["T1467284926140"][1:6]
