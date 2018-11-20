from django.test import TestCase

# Create your tests here.
import requests
import json
import hashlib
from urllib import request
import time



def genSignString(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, request.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode(encoding="utf-8"))
    return hash_md5.hexdigest().upper()


def qq_tran(msg):
    base_url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_texttrans"
    data = {
        "app_id": "2109258854",
        "app_key": "LSFaIB44cBW7dOKB",
        "time_stamp": int(time.time()),
        "nonce_str": int(time.time()),
        "text": msg,
        "type": 0,
    }
    sign_str = genSignString(data)
    data["sign"] = sign_str

    response = requests.get(url=base_url, params=data)
    print(response.url)
    print(response.text)


from wechatpy.client.api import WeChatMaterial
from wechatpy import WeChatClient


def get_file():
    client = WeChatClient("wx76342d45a73b2237", "5d7402129992ff3710be8f772198a068")
    wechat_material = WeChatMaterial(client=client)
    results = wechat_material.batchget("image")
    print(results)


def get_linshi_file():
    import base64
    from wechatpy.client.api import WeChatMedia
    client = WeChatClient("wx76342d45a73b2237", "5d7402129992ff3710be8f772198a068")
    media = WeChatMedia(client)
    # lTlNmiH1tvtUKkpDUfpz2CVC_UgbLkR_l-AyO45xnuNKKw9aHMV1GXdEHbhutwcQ
    info = media.download(media_id="07f89UfNiMnCsMDM_0oxXjxTZb9TQhyTapjHrOcAI4oZ7CHlyo1ys-Z4-E6wBDkt")
    print(info.content)
    print(str(base64.b64encode(info.content), encoding="utf-8"))
    print(base64.b64encode(info.content))


get_linshi_file()



