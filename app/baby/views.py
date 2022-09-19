from os import environ
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from baby.states import linebot,dailog_controller

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        event_contents = linebot.parse_event(body,signature)
        if len(event_contents)>0:
            event_content = event_contents[0]
            message = event_content['message']
            user_id = event_content['user_id']
            reply_token = event_content['reply_token']
            return_data = dailog_controller.process(message,user_id)
            linebot.reply_message(reply_token,return_data)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

