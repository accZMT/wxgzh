# -*- coding: utf-8 -*-
# python 3.6
"""
-------------------------------------------------
   File Name：     music
   Description :
   Author :       17971
   date：          2018/10/22
-------------------------------------------------
   Change Activity:
                   2018/10/22
-------------------------------------------------
"""

import requests
import json
import re
from urllib import parse


def get_music(msg):
    # 获取歌曲信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    base_url = "http://search.kuwo.cn/r.s?all={0}&ft=music& itemset=web_2013&client=kt&pn=1" \
               "&rn=1&rformat=json&encoding=utf8".format(msg.content)
    response = requests.get(base_url, headers=headers)
    result = response.text.replace("'", '"')
    data = json.loads(result)["abslist"][0]

    song_name = data["SONGNAME"]
    artist = data["ARTIST"]
    music_id = data["MUSICRID"]

    music_url = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={0}&format=aac|mp3&response=url".format(
        music_id)
    music_real_url = requests.get(music_url, headers=headers)
    song_url = music_real_url.text

    url = "http://player.kuwo.cn/webmusic/st/getNewMuiseByRid?rid={0}".format(music_id)
    music_response = requests.get(url, headers=headers)
    music_response.encoding = "utf-8"
    hq_song_url = re.findall(r"<song_url>(.*?)</song_url>", music_response.text, re.S)[0]

    return {
        "song_name": song_name,
        "artist": artist,
        "song_url": song_url,
        "hq_song_url": hq_song_url
    }


def get_wy_music(msg):
    url = "http://www.gj58.cn/music/index.php"
    pattern = re.compile(r'\s', re.S)
    form_data = {
        "input": pattern.sub('', msg.content[3:]),
        "type": "netease",
        "filter": "name",
        "page": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Host": "www.gj58.cn",
        "X-Requested-With": "XMLHttpRequest",
    }
    response = requests.post(url, data=form_data, headers=headers).json()
    result = response["data"][0]
    return {
        "link": result["link"],
        "title": result["title"],
        "author": result["author"],
        "url": result["url"]
    }

