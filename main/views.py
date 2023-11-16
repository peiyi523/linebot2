from django.shortcuts import render
from datetime import datetime
import json
import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from invoice import get_invoice_numbers, search_invoice_bingo

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)
start_invoice = False
numbers = []


@csrf_exempt
def callback(request):
    global start_invoice, numbers
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                message = event.message.text
                message_object = None
                # 判斷是否進行對獎模式
                if start_invoice:
                    if message == "0":
                        start_invoice = False
                        message_text = "離開發票對獎模式"
                    else:
                        message_text = search_invoice_bingo(message, numbers)
                        message_text += "\n==>請輸入下一組號碼(0:exit)"
                    message_object = TextSendMessage(text=message_text)
                elif message == "發票":
                    numbers = get_invoice_numbers()
                    message_text = "進入發票對獎模式==>\n本期最新發票對獎號碼:" + ",".join(numbers)
                    message_text += "\n請開始輸入您的發票號碼(後三碼):"
                    message_object = TextSendMessage(text=message_text)
                    start_invoice = True
                elif message == "你好":
                    message_object = TextSendMessage(text="jerry你好!")
                elif "樂透" in message:
                    reply_message = "預測號碼為:\n" + get_lottory_number()
                    message_object = TextSendMessage(text=reply_message)
                elif "捷運" in message:
                    if "台中" in message:
                        image_url = "https://upload.wikimedia.org/wikipedia/commons/f/f4/%E5%8F%B0%E4%B8%AD%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B7%9A%E5%9C%96_%282020.01%29.png"
                    elif "高雄" in message:
                        image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/kaohsiung/thumb_zh-Hant.png"
                    else:
                        image_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/taipei/20230214_zh.png"
                    message_object = ImageSendMessage(
                        original_content_url=image_url, preview_image_url=image_url
                    )
                else:
                    message_object = TextSendMessage(text="我不懂你的意思!")

                line_bot_api.reply_message(
                    event.reply_token,
                    message_object,
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"<h1>現在時刻:{now}</h1>")


# Create your views here.
def get_books(request):
    mybook = {1: "java-book", 2: "python-book", 3: "c-book"}

    return HttpResponse(json.dumps(mybook))


def get_lottory2(request):
    numbers = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    number_str = " ".join(map(str, numbers))
    return render(request, "lottory.html", {"numbers": number_str, "x": x})


def get_lottory_number():
    numbers = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    number_str = " ".join(map(str, numbers)) + f" 特別號:{x}"
    return number_str


def get_lottory(request):
    numbers = sorted(random.sample(range(1, 50), 6))
    print(numbers)
    x = random.randint(1, 50)
    number_str = " ".join(map(str, numbers)) + f" 特別號:{x}"
    return HttpResponse("<h1>本期預測號碼:</h1>" + "<h2>" + number_str + "</h2>")
