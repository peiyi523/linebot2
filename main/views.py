from django.shortcuts import render
import json
from datetime import datetime
import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
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
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text),
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


# Create your views here.
def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"<h1>現在時刻:{now}</h1>")


def get_books(request):
    mybook = {1: "java-book", 2: "python-book", 3: "c-book"}

    return HttpResponse(json.dumps(mybook))


def get_lottory2(request):
    numbers = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    numbers_str = " ".join(map(str, numbers))
    return render(request, "lottory.html", {"numbers": numbers_str, "x": x})


def get_lottory(request):
    numbers = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    numbers_str = " ".join(map(str, numbers)) + f" 特別號:{x}"
    return HttpResponse(f"<h1>本期預測號碼:</h1>" + "<h2>" + numbers_str + "</h2>")
