
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from linebot.models import MessageEvent, TextSendMessage
from baby.line_element import build_line_element
class LineBot:
    def __init__(self,token:str,secret:str):
        self.line_bot_api = LineBotApi(token)
        self.parser = WebhookParser(secret)
    def parse_event(self,body,signature):
        try:
            events = self.parser.parse(body, signature) 
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        contents = []
        for event in events:
            content = self.event_handler(event)
            if content!=None:
                contents.append(content)
        return contents

    def event_handler(self,event):
        # print('event',type(event),event)
        if isinstance(event,MessageEvent):
            user_id = event.source.__dict__['user_id']
            message = event.message.text
            reply_token = event.reply_token
        else:
            return None
        return {
            "user_id":user_id,
            "reply_token":reply_token,
            "message":message
        }
    
    def reply_message(self,token,data):
        line_element = build_line_element(data)
        try:
            self.line_bot_api.reply_message(token,line_element)
        except Exception as e:
            print(f"Failed to reply message:{str(e)}")
    def push_message(self,user_id,data):
        line_element = build_line_element(data)
        try:
            self.line_bot_api.push_message(user_id,line_element)
        except Exception as e:
            print(f"Failed to push message:{str(e)}")

        