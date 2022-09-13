from baby.models import BabyInfo,BabySitterInfo
import re
from baby.models import BabyInfo,BabySitterInfo
from baby.models import Feed,Daiper,Weight,Temperature
from baby.models import BabyCustoms,BabySitterCustoms
from baby.models import HeadLength, Height

import datetime
import time
import logging
from baby.reminder import reminder

def signup_user(user_id,sitter_name,baby_name):
    result = ""
    logging.info('signup')  
    #get baby object if not exist create one
    babys = BabyInfo.objects.filter(name=baby_name)
    if len(babys)==0:
        baby = BabyInfo(name=baby_name)
        baby.save()
        logging.info(f'signup baby:{baby_name}')
        result+='成功註冊寶寶資訊\n'
    else:
        baby = babys[0]
        result+='寶寶已註冊\n'

    #check if sitter exist if not create one
    sitters = BabySitterInfo.objects.filter(user_id=user_id,baby=baby)
    if len(sitters)==0:
        baby_sitter_info = BabySitterInfo(
            user_id=user_id,
            name=sitter_name,
            baby=baby
        )
        baby_sitter_info.save()
        logging.info(f'signup sitter:user_id:{user_id};sitter_name:{sitter_name}; baby_name:{baby_name}')
        result+='成功註冊\n'
    else:
        result+='重複註冊\n'
    
    return result



def get_sitter_from_user_id(user_id):
    result = BabySitterInfo.objects.filter(user_id=user_id)
    if len(result)>0:
        return result[0]
    else:
        return None



def admin_action(msg,user_id):
    action_txt,data = msg.split(';')
    
    if action_txt == '註冊使用者':
        sitter_name,baby_name = data.split('-')
        result = signup_user(user_id,sitter_name,baby_name)
        return result
    else:
        return "Invalid Message!"





def query_log(baby,period,query_types):
    #query_types => ['Feed','Daiper']

    #get start date time stamp
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    current_date = datetime.datetime.strptime(current_date,'%Y%m%d')

    start_date = current_date+datetime.timedelta(period)
    start_time_stamp = time.mktime(start_date.timetuple())

    content = {}
    for query_type in query_types:
        if query_type=='Daiper':
            db_rows = Daiper.objects.filter(baby=baby).order_by('time_stamp')
            
        elif query_type=='Feed':
            db_rows = Feed.objects.filter(baby=baby).order_by('time_stamp')
        elif query_type=='Weight':
            db_rows = Weight.objects.filter(baby=baby).order_by('time_stamp')
        elif query_type=='Temperature':
            db_rows = Temperature.objects.filter(baby=baby).order_by('time_stamp')
        elif query_type=='Height':
            db_rows = Height.objects.filter(baby=baby).order_by('time_stamp')
        elif query_type=='HeadLength':
            db_rows = HeadLength.objects.filter(baby=baby).order_by('time_stamp')
        content[query_type]=[]

        for db_row in db_rows:
            data_time_stamp = db_row.time_stamp
            if data_time_stamp>start_time_stamp:
                content[query_type].append(db_row)

    return content
def time_stamp_2_time_str(time_stamp,time_format):
    return datetime.datetime.fromtimestamp(time_stamp).strftime(time_format)
def format_log(content,baby):
    header = {
        "Daiper":"尿布",
        "Feed":"進食",
        "Weight":"體重",
        "Temperature":"體溫",
        "Height":"身高",
        "HeadLength":"頭圍"
    }
    result = f"寶寶:{baby.name}\n\n"
    dates = {}
    for query_type,db_rows in content.items():
        if len(db_rows)>0:
            section_result = f"{header[query_type]}:\n"
            dates[query_type]=[]
            for db_row in db_rows:
                time_format = '%Y/%m/%d'
                log_date = datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)
                if log_date not in dates[query_type]:
                    dates[query_type].append(log_date)
                    section_result+=f"\n{log_date}\n"
                if query_type=='Daiper':
                    log_str = format_log_daiper(db_row)
                elif query_type=='Feed':
                    log_str = format_log_feed(db_row)
                elif query_type=='Weight':
                    log_str = format_log_weight(db_row)
                elif query_type=='Temperature':
                    log_str = format_log_temperature(db_row)
                elif query_type=='Height':
                    log_str = format_log_height(db_row)
                elif query_type=='HeadLength':
                    log_str = format_log_head_length(db_row)
                section_result+=log_str
            section_result+='\n'
            result+=section_result
    return result

def summary_log(content):
    summary_all = {}
    for log_type,db_rows in content.items():
        summary=None
        if log_type=='Daiper':
            summary = summary_daiper(db_rows)
        elif log_type=='Feed':
            summary = summary_feed(db_rows)
        if summary is not None:
            summary_all[log_type]=summary
    return summary_all
def format_summary(summary_all):
    header = {
    "Daiper":"尿布",
    "Feed":"進食",
    "Weight":"體重",
    "Temperature":"體溫"
    }
    summary_content = "統計\n\n"
    for log_type,summary in summary_all.items():
        summary_str = f"{header[log_type]}:\n"
        for date_str,value in summary.items():
            summary_str+=f"{date_str}\n"
            if log_type=='Daiper':
                summary_str+=f'大便 : {value["Daiper2"]}次 小便 : {value["Daiper1"]}次\n'
            elif log_type=='Feed':
                summary_str+=f"奶量 : {value['Feed']} ml\n"
        summary_content+=summary_str
        summary_content+='\n'
    return summary_content
def summary_daiper(db_rows):
    #daiper times by day
    summary = {}
    for db_row in db_rows:
        db_date = datetime.datetime.fromtimestamp(db_row.time_stamp)
        #datetime object to datetime str=>20220831
        db_date_str = datetime.datetime.strftime(db_date,'%Y/%m/%d')
        if db_date_str not in summary:
            summary[db_date_str]={
                "Daiper1":0,
                "Daiper2":0
            }
        if db_row.change_type=='Daiper1':
            summary[db_date_str]['Daiper1']+=1
        else:
            summary[db_date_str]['Daiper2']+=1
    return summary

def summary_feed(db_rows):
    #summary feed ml sum all by date
    summary = {}
    for db_row in db_rows:
        db_date = datetime.datetime.fromtimestamp(db_row.time_stamp)
        #datetime object to datetime str=>20220831
        db_date_str = datetime.datetime.strftime(db_date,'%Y/%m/%d')
        volume = db_row.volume
        if db_date_str not in summary:
            summary[db_date_str]={"Feed":0}
        summary[db_date_str]['Feed']+=volume
    return summary



def format_log_daiper(db_row):
    time_format = '%H:%M'
    if db_row.change_type=='Daiper1':
        change_type='小便'
    else:
        change_type='大便'
    return f"{datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)} :{change_type}\n"

def format_log_feed(db_row):
    time_format = '%H:%M'
    return f"{datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)} :{int(db_row.volume)} ml\n"

def format_log_weight(db_row):
    time_format = '%H:%M'
    return f"{datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)} :{int(db_row.weight)} g\n"

def format_log_temperature(db_row):
    time_format = '%H:%M'
    return f"{datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)} :{db_row.temperature}度\n"
def format_log_height(db_row):
    time_format = '%H:%M'
    return f"{datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)} :{int(db_row.height)} cm\n"

def format_log_head_length(db_row):
    time_format = '%H:%M'
    return f"{datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)} :{int(db_row.head_length)} cm\n"

def search_action(msg,user_id):
    if 'Query_ALL'in msg:
        mode='ALL'
    else:
        mode='SUM'

    query_types = msg.split(f'Query_{mode}!')[1].split('@@')[0].split('&')
    period_txt = msg.split('@@')[-1]
    try:
        period = -1*int(period_txt)
    except:
        period = 1
    sitter = get_sitter_from_user_id(user_id)
    if sitter is None:
        return '尚未註冊使用者'
    baby=sitter.baby
    content = query_log(baby,period,query_types)
    summary_all = summary_log(content)
    
    if mode=="ALL":
        return format_log(content,baby)
    else:
        return format_summary(summary_all)

def log_action(msg,user_id):
    #msg=>Log!Milk**200@202208191010
    #msg=>Log!Daiper2**Daiper2@None
    sitter = get_sitter_from_user_id(user_id)
    if sitter is None:
        return '使用尚未註冊'
    baby =sitter.baby
    if '***' in msg:
        parse_element='***'
    else:
        parse_element='**'
    log_type = msg.split(parse_element)[0].replace('Log!','')
    data = msg.split(parse_element)[1]
    value,log_time = data.split('@')
    if log_time=='None':
        log_time_stamp = int(time.time())
    else:
        log_time_stamp = convert_log_time_2_timestamp(log_time)
    success,msg = log_data(sitter,baby,log_type,value,log_time_stamp)
    if success and log_time=='None':
        #when log current action, send msg 
        #log history will not send message
        send_log_message_to_all_user(sitter,baby,msg)
    return msg


def log_data(sitter,baby,log_type,value,log_time_stamp):
    success=True
    msg = "紀錄完成"
    if log_type in ['Milk']:
        log_feed(baby,sitter,log_time_stamp,value)
        msg = f"{sitter.name}紀錄{baby.name}喝奶{value}ml"
    elif log_type in ['Daiper2']:
        log_daiper(baby,sitter,log_time_stamp,value)
        msg = f"{sitter.name}紀錄{baby.name}大便一次"
    elif log_type in ['Daiper1']:
        log_daiper(baby,sitter,log_time_stamp,value)
        msg = f"{sitter.name}紀錄{baby.name}小便一次"
    elif log_type in ['Temperature']:
        log_temperature(baby,sitter,log_time_stamp,value)
        msg = f"{sitter.name}紀錄{baby.name}體溫{value}"
    elif log_type in ['Weight']:
        log_weight(baby,sitter,log_time_stamp,value)
        msg = f"{sitter.name}紀錄{baby.name}體重{value}g"
    elif log_type in ['Height']:
        log_height(baby,sitter,log_time_stamp,value)
        msg = f"{sitter.name}紀錄{baby.name}身高{value}cm"
    elif log_type in ['HeadLength']:
        log_head_length(baby,sitter,log_time_stamp,value)
        msg = f"{sitter.name}紀錄{baby.name}頭圍{value}cm"
    else:
        msg = "無效輸入!"
        success=False
    return success,msg

def convert_log_time_2_timestamp(time_str):
    return time.mktime(datetime.datetime.strptime(time_str,"%Y%m%d%H%M").timetuple())

def log_feed(baby,sitter,time_stamp,volume):
    feed = Feed(
    baby=baby,
    sitter=sitter,
    time_stamp=time_stamp,
    volume=volume
    )
    feed.save()
def log_daiper(baby,sitter,time_stamp,change_type):
    daiper = Daiper(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        change_type=change_type
    )
    daiper.save()

def log_temperature(baby,sitter,time_stamp,t):
    temperature = Temperature(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        temperature=t
    )
    temperature.save()
def log_weight(baby,sitter,time_stamp,w):
    weight = Weight(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        weight=w
    )
    weight.save()
def log_height(baby,sitter,time_stamp,h):
    weight = Height(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        height=h
    )
    weight.save()
def log_head_length(baby,sitter,time_stamp,hl):
    weight = HeadLength(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        head_length=hl
    )
    weight.save()
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)
from baby.element import (
        log_btn,
        day_btn,
        menu_btn,
        log_btn2,
        query_type_all_btn,
        query_type_sum_btn,
        reminder_btn,
        log_history_btn,
        query_btn,
        log_history_btn2,
        baby_customs_btn,
        settings_menu_btn,
        log_menu_btn,
        suggestions_menu_btn
    )

def parsing_query_data(msg,user_id):
    #return followup question => select period
    if '@@' == msg[-2:]:
        return True,day_btn
    else:
        return False,TextSendMessage(search_action(msg,user_id))
        
def parsing_query_next(msg,user_id):
    #return next action time 
    pass

def parsing_log_data(msg,user_id):

    #followup questions
    if '***' == msg[-3:]:
        if msg =='Log!Milk***':
            return True,TextSendMessage('請輸入奶量(ml)')
        elif msg=='Log!Weight***':
            return True,TextSendMessage('請輸入體重(g)')
        elif msg=='Log!Temperature***':
            return True,TextSendMessage('請輸入體溫(c)')

        elif msg=='Log!Height***':
            return True,TextSendMessage('請輸入身高(cm)')
        elif msg=='Log!HeadLength***':
            return True,TextSendMessage('請輸入頭圍(cm)')

        elif msg in ['Log!Daiper2***','Log!Daiper1***']:
            return True,TextSendMessage('請輸入日期,ex:@202208081716')
    elif '***' in msg:
        if '@' not in msg:
            return True,TextSendMessage('請輸入日期,ex:@202208081716')
        return False,TextSendMessage(log_action(msg,user_id))
    #followup questions
    elif '**'==msg[-2:]:
        if msg=='Log!Milk**':
            return True,TextSendMessage('請輸入奶量(ml)')
        elif msg=='Log!Daiper2**':
            msg = f'Log!Daiper2**Daiper2@None'
            return False,TextSendMessage(log_action(msg,user_id))
        elif msg=='Log!Daiper1**':
            msg = f'Log!Daiper1**Daiper1@None'
            return False,TextSendMessage(log_action(msg,user_id))
        elif msg=='Log!Weight**':
            return True,TextSendMessage('請輸入體重(g)')
        elif msg=='Log!Temperature**':
            return True,TextSendMessage('請輸入體溫(c)')
        elif msg=='Log!Height**':
            return True,TextSendMessage('請輸入身高(cm)')
        elif msg=='Log!HeadLength**':
            return True,TextSendMessage('請輸入頭圍(cm)')

    #log data has value 
    #Log!Milk**200
    else:
        if '@' not in msg:
            msg+='@None'
        return False,TextSendMessage(log_action(msg,user_id))

def parsing_reminder_data(msg,user_id):
    sitter = BabySitterInfo.objects.filter(user_id=user_id)[0]
    baby = BabyInfo.objects.filter(babysitterinfo=sitter)[0]
    baby_name = baby.name
    #need follow up Q
    #Reminder!Feed$$
    if '$$' == msg[-2:]:
        return True,TextSendMessage("請輸入提醒間隔(分鐘)")
    
    #already provide interval
    #Reminder!Feed$$30
    else:
        reminder_type = msg.split('$$')[0].split('!')[1]
        reminder_interval = 60*int(msg.split('$$')[1])
        if reminder_interval>0:
            reminder.add_reminder(baby_name,reminder_type,reminder_interval)
            return False,TextSendMessage("完成提醒設定")
        else:
            reminder.remove_reminder(baby_name,reminder_type)
            return False,TextSendMessage("取消提醒設定")
        


def menu_options(msg,user_id):
    menu_type = msg.split('Menu!')[-1]
    if menu_type=='Log':
        return False,log_btn
    elif menu_type=='Query':
        return False,query_btn
    elif menu_type=='Query_Type_SUM':
        return False,query_type_sum_btn
    elif menu_type=='Query_Type_ALL':
        return False,query_type_all_btn
    elif menu_type=='Log_WT':
        return False,log_btn2
    elif menu_type=='Reimder_Type':
        return False,reminder_btn
    elif menu_type=='Log_History':
        return False,log_history_btn
    elif menu_type=='Log_History_WT':
        return False,log_history_btn2
    elif menu_type=='Baby_Customs':
        return False,baby_customs_btn
    elif menu_type=='Settings':
        return False,settings_menu_btn
    elif menu_type=='Logs':
        return False,log_menu_btn
    elif menu_type=='Suggestions':
        return False,suggestions_menu_btn


def message_parsing(msg,user_id):
    reminder.start_thread()
    print('msg',msg,'user_id',user_id)
    if 'Menu!' in msg:
        return menu_options(msg,user_id)
    #button question
    if '**' in msg:
        return parsing_log_data(msg,user_id)
    #reminder settings
    elif '$$' in msg:
        return parsing_reminder_data(msg,user_id)
    #query
    elif '@@' in msg:
        return parsing_query_data(msg,user_id)
    #admin actions
    elif ';' in msg:
        return False,TextSendMessage(admin_action(msg,user_id))
    # elif '~~' in msg:
    #     return False,parsing_query_next(msg,user_id)
    #suggestions
    elif '##' in msg:
        return parsing_suggestions(msg,user_id)
    #set baby customs : feed interval...
    elif '^^' in msg:
        return parsing_baby_custom(msg,user_id)
    else:
        #enter log btn
        return False,menu_btn



def send_log_message_to_all_user(log_sitter,baby,msg):
    sitters = BabySitterInfo.objects.filter(baby=baby)
    log_sitter_id = log_sitter.user_id
    for sitter in sitters:
        user_id = sitter.user_id
        if user_id !=log_sitter_id:
            reminder.send_message(user_id,msg)


def parsing_suggestions(msg,user_id):
    sitter = get_sitter_from_user_id(user_id)
    baby=sitter.baby
    suggestion_type = msg.split('!')[-1].split('##')[0]
    baby_customs = BabyCustoms.objects.filter(baby=baby)
    if len(baby_customs)>0:
        baby_customs=baby_customs[0]
    else:
        return False,TextSendMessage("請先設定相關資料")
    if suggestion_type=='Feed':
        baby_weights = Weight.objects.filter(baby=baby).order_by('-time_stamp')
        if len(baby_weights)>0:
            baby_weight=baby_weights[0].weight
            feed_vol = [round(baby_weight*120/1000),round(baby_weight*150/1000)]
            return_msg = f"根據最後一次體重{baby_weight}g\n每日建議奶量{feed_vol[0]}-{feed_vol[1]}ml"
            feed_frequency = baby_customs.feed_frequency
            if feed_frequency!=None:
                return_msg+=f"\n每餐建議奶量{round(feed_vol[0]/feed_frequency)}-{round(feed_vol[1]/feed_frequency)}ml"
        else:
            return_msg="尚未設定體重"
    elif suggestion_type=='FeedTime':
        feeds = Feed.objects.filter(baby=baby).order_by('-time_stamp')
        feed_interval = baby_customs.feed_interval
        if len(feeds)>0:
            last_feed_time = datetime.datetime.fromtimestamp(int(feeds[0].time_stamp))
            next_feed_times = []
            for i in range(2):
                next_feed_time = last_feed_time+datetime.timedelta(minutes=(feed_interval*(i+1)))
                next_feed_times.append(next_feed_time)
            time_format = '%H:%M'
            return_msg = f"下次餵奶時間:{datetime.datetime.strftime(next_feed_times[0],time_format)}\n下下次餵奶時間:{datetime.datetime.strftime(next_feed_times[1],time_format)}"
    elif suggestion_type=='Sleep':
        birthday = baby.birthday
        return_msg = suggestion_sleep_time_table(birthday)
    return False,TextSendMessage(return_msg)

def parsing_baby_custom(msg,user_id):
    
    sitter = get_sitter_from_user_id(user_id)
    
    set_item = msg.split('!')[-1].split('^^')[0]
    if '^^' == msg[-2:]:
        #SetBabyCm!Birthday^^
        questions = {
            "Birthday":"請輸入生日ex:20220806",
            "FeedInterval":"請輸入餵奶間隔(分鐘)ex:240",
            "FeedFrequency":"請輸入每日餵奶次數ex:6",
            "Gender":"請輸入性別ex:男/女"
        }
        return True,TextSendMessage(questions[set_item])
    else:
        #SetBabyCm!Birthday^^20220806
        baby=sitter.baby
        baby_customs = BabyCustoms.objects.filter(baby=baby)
        value = msg.split('^^')[-1]
        if set_item=='Check':
            if len(baby_customs)>0:
                baby_customs=baby_customs[0]
                msg = f"生日:\n{baby_customs.birthday}\n餵奶間隔:\n{baby_customs.feed_interval}\n每日餵奶次數:\n{baby_customs.feed_frequency}"
            else:
                msg = '設定尚未建置'
            return False,TextSendMessage(msg)
        
        if len(baby_customs)>0:
            if set_item =='Birthday':
                birthday = datetime.datetime.strftime(datetime.datetime.strptime(value,'%Y%m%d'),'%Y-%m-%d')
                baby_info = BabyInfo.objects.filter(name=baby.name)
                baby_info.update(birthday=birthday)

            elif set_item=='FeedInterval':
                baby_customs.update(feed_interval=int(value))
            elif set_item=='FeedFrequency':
                baby_customs.update(feed_frequency=int(value))
            elif set_item=='Gender':
                if value=='男':
                    gender='boy'
                    # gender=True
                else:
                    gender='girl'
                    # gender=False
                baby_info = BabyInfo.objects.filter(name=baby.name)
                baby_info.update(gender=gender)
            return False,TextSendMessage("資料已更新")
        else:
            birthday,feed_interval,feed_frequency,gender=None,None,None,None
            if set_item =='Birthday':
                birthday = datetime.datetime.strftime(datetime.datetime.strptime(value,'%Y%m%d'),'%Y-%m-%d')
                baby_info = BabyInfo.objects.filter(name=baby.name)
                baby_info.update(birthday=birthday)
            elif set_item=='FeedInterval':
                feed_interval=int(value)
            elif set_item=='FeedFrequency':
                feed_frequency=int(value)
            elif set_item=='Gender':
                if value=='男':
                    gender='boy'
                    # gender=True
                else:
                    gender='girl'
                    # gender=False
                baby_info = BabyInfo.objects.filter(name=baby.name)
                baby_info.update(gender=gender)
            baby_customs = BabyCustoms(
                baby=baby,
                feed_interval=feed_interval,
                feed_frequency=feed_frequency,
            )
            baby_customs.save()
            return False,TextSendMessage("資料已建置")



def suggestion_sleep_time_table(birthday):
    date_delta = int((datetime.datetime.now().date()-birthday).days)
    sleep_time_table = {
        "0-14":{
            "total":"17.5-18.5",
            "day_sleep":"5.5-6.5",
            "night_sleep":"12"
        },
        "14-28":{
            "total":"17-18",
            "day_sleep":"5-6",
            "night_sleep":"12"
        },
        "28-42":{
            "total":"17",
            "day_sleep":"5",
            "night_sleep":"12"
        },
        "42-56":{
            "total":"16",
            "day_sleep":"4",
            "night_sleep":"12"
        },
        "56-90":{
            "total":"15.5",
            "day_sleep":"3.5",
            "night_sleep":"12"
        },
        "90-180":{
            "total":"14.5-15",
            "day_sleep":"2.5-3",
            "night_sleep":"12"
        },
        "180-270":{
            "total":"14.5",
            "day_sleep":"2.5",
            "night_sleep":"12"
        },
        "270-365":{
            "total":"14-14.5",
            "day_sleep":"2-2.5",
            "night_sleep":"12"
        }
    }
    for k,v in sleep_time_table.items():
        start,end = [int(x) for x in k.split('-')]
        if date_delta>start and date_delta<=end:
            return f"建議睡眠時間:\n總睡眠時數:{v['total']}小時\n白天睡眠時數:{v['day_sleep']}小時\n晚上睡眠時數:{v['night_sleep']}小時"
    return "無法顯示"