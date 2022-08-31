
from csv import Dialect
import datetime
import threading
from baby.models import Daiper,Feed,BabyInfo,BabySitterInfo
import time
from linebot import LineBotApi, WebhookParser
import os
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
assert LINE_CHANNEL_ACCESS_TOKEN!=''
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)
class Reminder:
    def __init__(self,line_bot_api):
        self.line_bot_api=line_bot_api
        self.reminder_data = {}
        self.check_interval = 600
        self.sent_reminder_list = {}
    def gen_data_key(self,baby_name,reminder_type):
        return f"{baby_name}****{reminder_type}"
    def split_data_key(self,data_key):
        return data_key.split('****')
    def add_reminder(self,baby_name,reminder_type,interval):
        self.reminder_data[self.gen_data_key(baby_name,reminder_type)]=interval
    
    def remove_reminder(self,baby_name,reminder_type):
        data_key = self.gen_data_key(baby_name,reminder_type)
        if data_key in self.reminder_data:
            del self.reminder_data[data_key]
            if data_key in self.sent_reminder_list:
                del self.sent_reminder_list[data_key]
    def _check_last_time(self,baby_name,reminder_type,interval):
        babies = BabyInfo.objects.filter(name=baby_name)
        if len(babies)>0:
            baby=babies[0]
            if reminder_type=='Daiper':
                last_row = Daiper.objects.filter(baby=baby).order_by('-time_stamp')[0]
            elif reminder_type=='Feed':
                last_row = Feed.objects.filter(baby=baby).order_by('-time_stamp')[0]

            time_delta = time.time()-last_row.time_stamp

            if time_delta>interval:
                return last_row.time_stamp

    def check(self):
        print('check')
        for data_key,interval in self.reminder_data.items():
            baby_name,reminder_type = self.split_data_key(data_key)
            last_time_stamp = self._check_last_time(baby_name,reminder_type,interval)
            if last_time_stamp is not None and self.check_sent_list(data_key,last_time_stamp)==False:
                self.remind_user(baby_name,reminder_type,last_time_stamp)
                self.sent_reminder_list[data_key]=last_time_stamp
    def check_sent_list(self,data_key,last_time_stamp):
        #check if sent already
        if data_key in self.sent_reminder_list:
            return last_time_stamp==self.sent_reminder_list[data_key]
        else:
            return False
    def remind_user(self,baby_name,reminder_type,last_time_stamp):
        baby = BabyInfo.objects.filter(name=baby_name)[0]
        last_time = datetime.datetime.fromtimestamp(last_time_stamp).strftime('%Y/%m/%d %H:%M')
        if reminder_type=='Daiper':
            msg = f"請記得換尿布，上次換尿布時間為{last_time}"
        elif reminder_type=='Feed':
            msg = f'請記得餵奶，上次餵奶時間為{last_time}'
        
        for sitter in BabySitterInfo.objects.filter(baby=baby):
            sitter_id = sitter.user_id
            self.send_message(sitter_id,msg)

    def send_message(self,user_id,message):
        self.line_bot_api.push_message(user_id,TextSendMessage(text=message))


    def loop_check(self):
        while True:
            self.check()
            time.sleep(self.check_interval)

reminder = Reminder(line_bot_api)
t = threading.Thread(target=reminder.loop_check)
t.start()