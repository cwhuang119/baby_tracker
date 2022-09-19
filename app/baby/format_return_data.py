

import datetime
from urllib import request

def format_query_all_content(query_content,baby):
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
    for query_type,db_rows in query_content.items():
        if len(db_rows)>0:
            section_result = f"{header[query_type]}:\n"
            dates[query_type]=[]
            for db_row in db_rows:
                time_format = '%Y/%m/%d'
                log_date = datetime.datetime.fromtimestamp(db_row.time_stamp).strftime(time_format)
                if log_date not in dates[query_type]:
                    dates[query_type].append(log_date)
                    section_result+=f"\n{log_date}\n"
                section_result+=db_row.format_log_str()
            section_result+='\n'
            result+=section_result
    return result

def format_query_sum_content(query_content,baby):
    summary_all = {}
    for query_type,db_rows in query_content.items():
        summary=None
        if query_type=='Daiper':
            summary = summary_daiper(db_rows)
        elif query_type=='Feed':
            summary = summary_feed(db_rows)
        if summary is not None:
            summary_all[query_type]=summary
    return format_summary(summary_all,baby)
def format_summary(summary_all,baby):
    header = {
    "Daiper":"尿布",
    "Feed":"進食",
    "Weight":"體重",
    "Temperature":"體溫"
    }
    summary_content = f"寶寶{baby.name} 統計紀錄\n\n"
    for log_type,summary in summary_all.items():
        summary_str = f"{header[log_type]}:\n"
        for date_str,value in summary.items():
            summary_str+=f"{date_str}\n"
            if log_type=='Daiper':
                summary_str+=f'大便 : {value["2"]}次 小便 : {value["1"]}次\n'
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
                "1":0,
                "2":0
            }
        if db_row.change_type in ['Daiper1','1']:
            summary[db_date_str]['1']+=1
        elif db_row.change_type in ['Daiper2','2']:
            summary[db_date_str]['2']+=1
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

def format_log_str(db_row):
    return db_row.format_log_str()

def gen_line_ask_time():
    return "請輸入日期與時間ex:202208081717"

def gen_line_log_failed():
    return "登記失敗，請重新操作！"

def gen_lines_Log(baby,sitter,request_type,request_data,follow_up):

    follow_up_lines = {
        "Feed":"請輸入奶量(ml)",
        "Weight":"請輸入體重(g)",
        "Temperature":"請輸入體溫(c)",
        "Height":"請輸入身高(cm)",
        "HeadLength":"請輸入頭圍(cm)"
    }

    success_lines = {
        "Feed":["喝奶","ml"],
        "Weight":["體重","g"],
        "Temperature":["體溫","度"],
        "Height":["身高","cm"],
        "HeadLength":["頭圍","cm"],
    }

    # gen follow up lines
    if follow_up:
        return follow_up_lines[request_type]
    #gen success lines
    else:
        baby_name = baby.name
        sitter_name = sitter.name
        msg = f"{sitter_name}紀錄{baby_name}"
        if request_type=='Daiper':
            if request_data=='1':
                change_type = '小便'
            else:
                change_type = '大便'
            msg+=f"{change_type}一次"
        else:
            msg+=f"{success_lines[request_type][0]}{request_data}{success_lines[request_type][1]}"
        return msg


def gen_lines_babycustoms(baby,sitter,request_type,request_data,follow_up):
    follow_up_lines =  {
        "Birthday":"請輸入生日ex:20220806",
        "FeedInterval":"請輸入餵奶間隔(分鐘)ex:240",
        "FeedFrequency":"請輸入每日餵奶次數ex:6",
        "Gender":"請輸入性別ex:男/女"
    }
    if follow_up:
        return follow_up_lines[request_type]
    else:
        ## SETUP BABY CUSTOM
        return "資料已建置"



def gen_lines_suggestions(baby,sitter,request_type,baby_customs,last_weight,last_feed):
    if baby_customs is None:
        return '寶寶資料尚未建置'
    if request_type=='FeedVolume':
        if last_weight is None:
            return '寶寶資料尚未建置(體重)'
        feed_vol = [round(last_weight.weight*120/1000),round(last_weight.weight*150/1000)]
        return_msg = f"根據最後一次體重{last_weight.weight}g\n每日建議奶量{feed_vol[0]}-{feed_vol[1]}ml"
        feed_frequency = baby_customs.feed_frequency
        if feed_frequency!=None:
            return_msg+=f"\n每餐建議奶量{round(feed_vol[0]/feed_frequency)}-{round(feed_vol[1]/feed_frequency)}ml"
        return return_msg

    elif request_type=='NextFeed':
        if last_feed is None:
            return "找不到最後一次餵奶紀錄"
        feed_interval = baby_customs.feed_interval
        last_feed_time = datetime.datetime.fromtimestamp(int(last_feed.time_stamp))
        next_feed_times = []
        for i in range(2):
            next_feed_time = last_feed_time+datetime.timedelta(minutes=(feed_interval*(i+1)))
            next_feed_times.append(next_feed_time)
        time_format = '%H:%M'
        return_msg = f"下次餵奶時間:{datetime.datetime.strftime(next_feed_times[0],time_format)}\n下下次餵奶時間:{datetime.datetime.strftime(next_feed_times[1],time_format)}"
        return return_msg

    elif request_type=='SleepingTime':
        birthday = baby.birthday
        return_msg = suggestion_sleep_time_table(birthday)
        return return_msg
    
    return '建議失敗'

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