from os import environ
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from baby.dialog import message_parsing

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
global chat_cache
chat_cache = {}

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature) 
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            user_id = event.source.__dict__['user_id']
            
            if isinstance(event, MessageEvent): 
                # text message
                message = event.message.text

                # check if there is message in cache
                # if exist will concate last message with this message
                if user_id in chat_cache:
                    print(chat_cache[user_id])
                    message = chat_cache[user_id] + message

                #parsing message and go to action 
                follow_up,result = message_parsing(message,user_id)

                #if follow up if True will store this message for later usage
                if follow_up:
                    chat_cache[user_id]=message
                else:
                    if user_id in chat_cache:
                        del chat_cache[user_id]
                #reply message , result will be line message object
                line_bot_api.reply_message(  
                    event.reply_token,
                    result
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

