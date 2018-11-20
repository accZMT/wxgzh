# -*- coding: utf-8 -*-
# python 3.6
"""
-------------------------------------------------
   File Name：     utils
   Description :
   Author :       17971
   date：          2018/10/23
-------------------------------------------------
   Change Activity:
                   2018/10/23
-------------------------------------------------
"""
from wechatpy import create_reply
import requests
import hashlib
from urllib import request
import json
import time
from utils.music import get_wy_music
from wechatpy.replies import MusicReply
from wechatpy import WeChatClient
from mysite.settings import APP_ID, APP_SECRET, app_id, app_key


def do_text_reply(msg):
    """
    回复文本消息
    :param msg:
    :return:
    """
    if msg.type == "text":
        if msg.content.startswith("天气"):
            reply = weather(msg)
        elif msg.content.startswith("音乐"):
            reply = MusicReply(message=msg)
            data = get_wy_music(msg)
            reply.title = data.get("title", '')
            reply.description = data.get("author", '')
            reply.thumb_media_id = "mHTllUWQjRS27E5rctmlCIJ991IhUn2EQ1NdBTP44g8"
            reply.music_url = data.get("url", '')
            reply.hq_music_url = data.get("url", '')
        elif msg.content == "猜谜语":
            reply = guess(msg)
        elif msg.content.startswith("翻译"):
            reply = create_reply(qq_tran(msg), message=msg)
        else:
            content = "------功能详情------\n回复关键字即可 如：\n" \
                      "[天气：郑州]\n[翻译：你好]\n[猜谜语]\n[音乐：天空之城]\n说句语音试一试O(∩_∩)O~~"
            reply = create_reply(content, message=msg)
        return reply


def weather(msg):
    """
    获取天气信息
    :param msg:
    :return:
    """
    if msg.content == "天气":
        current_url = 'https://api.map.baidu.com/location/ip?ak=KHkVjtmfrM6NuzqxEALj0p8i1cUQot6Z'
        response = requests.get(current_url).json()
        city = response['content']['address_detail']['city']
    else:
        city = msg.content[3:].strip()
    url = 'http://api.map.baidu.com/telematics/v3/weather?location={}&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'.format(city)
    result = requests.get(url).json()
    if 'error' in result:
        if result['error'] == 0:
            data = result['results'][0]['weather_data'][0]
            context = "城市：{0}\n今日天气：{1}\n温度：{2}\n风力：{3}\n天气：{4}\n---未来天气---\n".format(city, data["date"], data["temperature"], data["wind"], data["weather"])
            for data in result['results'][0]['weather_data'][1:]:
                context += "日期：{}\n温度：{}\n风力：{}\n天气：{}\n".format(data["date"], data["temperature"], data["wind"], data["weather"])
        else:
            context = '无法获取当前城市天气预报'
    else:
        context = '天配额超限，限制访问'
    return create_reply(context, msg)


def guess(msg):
    """
    猜谜语
    :param msg:
    :return:
    """
    url = "http://api.shujuzhihui.cn/api/riddle/rand?appKey=02796fb90c2d405eb90b3039866817d9"
    response = requests.get(url)
    results = json.loads(response.text)
    reply_content = '测测你的小脑袋~~~~~~~~答案在最后(⊙o⊙)哦\n'
    answer_text = "\n" * 10 + "答案：\n"
    if results["ERRORCODE"] == '0':
        contents = results["RESULT"]["contentlist"]
        for index, content in enumerate(contents[:10]):
            answer = content["answer"]
            typename = content["typeName"]
            title = content["title"]
            reply_content += "第{0}条\n提示：{1}\n{2}\n".format(index + 1, typename, title)
            answer_text += "第{0}条\n{1}\n".format(index + 1, answer)
    reply_content += answer_text
    return create_reply(reply_content, message=msg)


def genSignString(parser):
    """
    根据文档要求算出必要参数sign
    :param parser:
    :return:
    """
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, request.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']
    hash_md5 = hashlib.md5(sign_str.encode(encoding="utf-8"))
    return hash_md5.hexdigest().upper()


def qq_tran(msg):
    """
    文本翻译
    :param msg:
    :return:
    """
    base_url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_texttrans"
    data = {
        "app_id": app_id,
        "app_key": app_key,
        "time_stamp": int(time.time()),
        "nonce_str": int(time.time()),
        "text": msg.content[3:].strip(),
        "type": 0,
    }
    sign_str = genSignString(data)
    data["sign"] = sign_str

    response = requests.get(url=base_url, params=data)
    result = json.loads(response.text)
    if result["ret"] == 0:
        return result["data"]["trans_text"]
    else:
        return "你输入的内容无法翻译"


def get_speech_chunk(msg):
    """
    根据文档要求，得出session_id, speech_chunk
    :param msg:
    :return:
    """
    import base64
    from wechatpy.client.api import WeChatMedia
    client = WeChatClient(APP_ID, APP_SECRET)
    media = WeChatMedia(client)
    info = media.download(media_id=msg.media_id)
    md5 = hashlib.md5(info.content)
    # 返回session_id, speech_chunk
    return md5.hexdigest().upper(), str(base64.b64encode(info.content), "utf-8")


def speech_tran(msg):
    """
    语音翻译
    :param msg:
    :return:
    """
    base_url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_speechtranslate"
    session_id, speech_chunk = get_speech_chunk(msg)
    data = {
        "app_id": app_id,
        "app_key": app_key,
        "end": 1,
        "format": 3,
        "nonce_str": str(time.time()),
        "seq": 0,
        "session_id": session_id,
        "source": "zh",
        "speech_chunk": speech_chunk,
        "target": "en",
        "time_stamp": int(time.time()),
    }
    sign_str = genSignString(data)
    data["sign"] = sign_str
    response = requests.post(base_url, data=data)
    result = response.json()
    if result["ret"] == 0:
        return result["data"]["target_text"]
    else:
        return "你输入的内容无法翻译"


def do_event_reply(msg):
    """
    当用户关注公众号发送消息
    :param msg:
    :return:
    """
    if msg.event == "subscribe":
        content = "------功能详情------\n回复关键字即可 如：\n" \
                  "[天气：郑州]\n[翻译：你好]\n[猜谜语]\n[音乐：天空之城]"
        reply = create_reply("你长得那么好看，谢谢关注\n输入关键字即可参加游戏(⊙o⊙)哦\n" + content, msg)
    # elif msg.event == "unsubscribe":
    #     pass
    else:
        reply = create_reply("我们不知道你说的啥", msg)
    return reply


