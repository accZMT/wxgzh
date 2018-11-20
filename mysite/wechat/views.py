from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy.parser import parse_message
from wechatpy.replies import create_reply, ArticlesReply
from wechatpy.client import WeChatClient
from wechat.utils import do_text_reply, do_event_reply, speech_tran
from wechat.models import MaterialModel
from wechatpy.replies import ImageReply, MusicReply
from wechatpy.client.api import WeChatMaterial
from utils.news import get_news
from mysite.settings import APP_ID, APP_SECRET

TOKEN = "acczmt"
IMG_MEDIA_ID = ''


@csrf_exempt
def handle_wx(request):
    global IMG_MEDIA_ID
    # GET 方式用于微信的公共平台绑定验证
    if request.method == "GET":
        signature = request.GET.get("signature", "")
        timestamp = request.GET.get("timestamp", "")
        nonce = request.GET.get("nonce", "")
        echo_str = request.GET.get("echostr", "")
        try:
            check_signature(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = "error"
        response = HttpResponse(echo_str)
        return response
    if request.method == "POST":

        msg = parse_message(request.body)
        if msg.type == "text":
            reply = do_text_reply(msg)
        elif msg.type == 'image':
            IMG_MEDIA_ID = msg.media_id
            reply = create_reply("图片已收到" + msg.media_id, msg)
        elif msg.type == 'event':
            if msg.key == "func_detail":
                content = "------功能详情------\n回复关键字即可 如：\n" \
                          "[天气：郑州]\n[翻译：你好]\n[猜谜语]\n[音乐：天空之城]\n说句语音试一试O(∩_∩)O~~"
                reply = create_reply(content, message=msg)
            elif msg.key == "daily_image":
                reply = ImageReply(message=msg)
                reply.media_id = IMG_MEDIA_ID
            elif msg.key == "daily_music":
                reply = MusicReply(message=msg)
                reply.title = "偏偏喜欢你"
                reply.description = "陈百强"
                reply.thumb_media_id = IMG_MEDIA_ID
                reply.music_url = "http://bd.kuwo.cn/yinyue/28409674"
                reply.hq_music_url = "http://bd.kuwo.cn/yinyue/28409674"
            elif msg.key == "daily_push":
                reply = ArticlesReply(message=msg)
                for data in get_news():
                    reply.add_article({
                        'title': data["title"],
                        'description': data["source"],
                        'image': data["imgsrc"],
                        'url': data["url"]
                    })
            else:
                reply = do_event_reply(msg)
        elif msg.type == 'voice':
            result = speech_tran(msg)
            reply = create_reply(result, msg)
        else:
            reply = create_reply('你发送的消息已经收到', msg)
        response = HttpResponse(reply.render(), content_type="application/html")
        return response
"""
VoiceMessage(OrderedDict([('ToUserName', 'gh_0e4a6b593687'), ('FromUserName', 'ol_bn1YGOiEIIW-r2_tnWpbKBA7U'), ('CreateTime', '1540554250
'), ('MsgType', 'voice'), ('MediaId', 'lTlNmiH1tvtUKkpDUfpz2CVC_UgbLkR_l-AyO45xnuNKKw9aHMV1GXdEHbhutwcQ'), ('Format', 'amr'), ('MsgId', '
6616630121882864813'), ('Recognition', None)]))

"""


def create_menu(request):
    """
    自定义菜单
    :param request:
    :return:
    """
    client = WeChatClient(APP_ID, APP_SECRET)
    client.menu.create({
        "button": [
            {
                "type": "click",
                "name": "功能详情",
                "key": "func_detail"
            },
            {
                "name": "每日推送",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "每日音乐",
                        "key": "daily_music"
                    },
                    {
                        "type": "click",
                        "name": "每日新闻",
                        "key": "daily_push"
                    },
                    {
                        "type": "click",
                        "name": "每日美图",
                        "key": "daily_image"
                    }
                ]
            },

            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "个人博客",
                        "url": "https://acczmt.top"
                    },
                    {
                        "type": "view",
                        "name": "Github",
                        "url": "https://github.com/accZMT"
                    },
                    {
                        "type": "click",
                        "name": "关注我",
                        "key": "V1001_GOOD"
                    }
                ]
            }
        ]
    })

    return HttpResponse("ok")


def add_material(request):
    if request.method == "GET":
        return render(request, 'add_media.html')
    if request.method == "POST":
        # 上传临时素材并且存入数据库， 注意上穿的图片名字不能是中文
        media_type = request.POST.get("media_type", "")
        media_file = request.FILES.get("media_file")
        title = request.POST.get("title", "")
        introduction = request.POST.get("introduction", "")

        # 主要作用获取access_token
        client = WeChatClient(APP_ID, APP_SECRET)
        from wechatpy.client.api import WeChatMedia
        media = WeChatMedia(client)
        info = media.upload(media_type, media_file)

        material = MaterialModel()
        material.media_type = media_type
        material.title = title
        material.introduction = introduction
        material.media_id = info["media_id"]
        material.save()
        return HttpResponse("OK")


@csrf_exempt
def add_permanent_material(request):
    """
    上传永久素材
    :param request:
    :return:
    """
    media_type = request.POST.get("media_type", "")
    media_file = request.FILES.get("media_file")
    title = request.POST.get("title", "")
    introduction = request.POST.get("introduction", "")
    client = WeChatClient(APP_ID, APP_SECRET)
    from wechatpy.client.api import WeChatMaterial

    mater = WeChatMaterial(client)
    info = mater.add(media_type, media_file, title, introduction)
    print(info)

    """
    {'media_id': 'mHTllUWQjRS27E5rctmlCAqaV-sXOTgvpGx7ST8h2m4', 
      'url': 'http://mmbiz.qpic.cn/mmbiz_jpg/iap38Z2kZ6R4giciaKIWR9LdXXO3JL1eVjecQECB1nCO3EA9jEQjFUuDJYaJn0VFpDunaKSibePiafUmgqniaJlkUciaA/0?wx_fmt=jpeg'}

    """

    return HttpResponse("OK")


def get_file():
    client = WeChatClient(APP_ID, APP_SECRET)
    wechat_material = WeChatMaterial(client=client)
    results = wechat_material.batchget("image")
    print(results)




