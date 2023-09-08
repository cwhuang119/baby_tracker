

import datetime
import time

from baby.models import BabyCustoms
from baby.models import BabyInfo
from baby.models import BabySitterInfo
from baby.models import Daiper,Weight,HeadLength,Height,Feed,Temperature



def get_sitter_from_user_id(user_id):
    result = BabySitterInfo.objects.filter(user_id=user_id)
    if len(result)>0:
        return result[0]
    else:
        return None




def get_sitter_baby(user_id):
    sitter = get_sitter_from_user_id(user_id)
    if sitter !=None:
        return sitter,sitter.baby
    else:
        return None,None

def query_log(baby,query_types,period):
    period = int(period)*-1
    #get start date time stamp
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    current_date = datetime.datetime.strptime(current_date,'%Y%m%d')

    start_date = current_date+datetime.timedelta(period)
    start_time_stamp = time.mktime(start_date.timetuple())
    content = {}
    for query_type in query_types:
        db_rows = eval(f"{query_type}.objects.filter(baby=baby).order_by('time_stamp')")
        content[query_type]=[]

        for db_row in db_rows:
            data_time_stamp = db_row.time_stamp
            if data_time_stamp>start_time_stamp:
                content[query_type].append(db_row)
    return content

def log_data(baby,sitter,log_type,time_stamp,value):
    
    return eval(f"log_{log_type}(baby,sitter,time_stamp,value)")


def log_Feed(baby,sitter,time_stamp,value):
    feed = Feed(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        volume=value
    )

    feed.save()
    return feed is not None

def log_Daiper(baby,sitter,time_stamp,value):
    daiper = Daiper(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        change_type=value
    )
    daiper.save()
    return daiper is not None
def log_Temperature(baby,sitter,time_stamp,value):
    temperature = Temperature(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        temperature=value
    )
    temperature.save()
    return temperature is not None
def log_Weight(baby,sitter,time_stamp,value):
    weight = Weight(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        weight=value
    )
    weight.save()
    return weight is not None
def log_Height(baby,sitter,time_stamp,value):
    height = Height(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        height=value
    )
    height.save()
    return height is not None
def log_HeadLength(baby,sitter,time_stamp,value):
    head_length = HeadLength(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        head_length=value
    )
    head_length.save()
    return head_length is not None


def set_babycustoms(baby,sitter,request_type,request_data):
    baby_customs = BabyCustoms.objects.filter(baby=baby)
    if len(baby_customs)>0:
        if request_type =='Birthday':
            birthday = datetime.datetime.strftime(datetime.datetime.strptime(request_data,'%Y%m%d'),'%Y-%m-%d')
            baby_info = BabyInfo.objects.filter(name=baby.name)
            baby_info.update(birthday=birthday)
        elif request_type=='FeedInterval':
            baby_customs.update(feed_interval=int(request_data))
        elif request_type=='FeedFrequency':
            baby_customs.update(feed_frequency=int(request_data))
        elif request_type=='Gender':
            if request_data=='男':
                gender='boy'
                # gender=True
            else:
                gender='girl'
                # gender=False
        return True
    else:
        baby_info = BabyInfo.objects.filter(name=baby.name)
        baby_info.update(gender=gender)
        birthday,feed_interval,feed_frequency,gender=None,None,None,None
        if request_data =='Birthday':
            birthday = datetime.datetime.strftime(datetime.datetime.strptime(request_data,'%Y%m%d'),'%Y-%m-%d')
            baby_info = BabyInfo.objects.filter(name=baby.name)
            baby_info.update(birthday=birthday)
        elif request_data=='FeedInterval':
            feed_interval=int(request_data)
        elif request_data=='FeedFrequency':
            feed_frequency=int(request_data)
        elif request_data=='Gender':
            if request_data=='男':
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
        return True


def get_baby_customs(baby):
    baby_customs = BabyCustoms.objects.filter(baby=baby)
    if len(baby_customs)>0:
        return baby_customs[0]
    else:
        return None


def get_last_weight(baby):
    baby_weights = Weight.objects.filter(baby=baby).order_by('-time_stamp')
    if len(baby_weights)>0:
        return baby_weights[0]

def get_last_feed(baby):
    feeds = Feed.objects.filter(baby=baby).order_by('-time_stamp')

    if len(feeds)>0:
        return feeds[0]


def register_baby(baby_name):
    # check if baby exists
    baby_info = BabyInfo.objects.filter(name=baby_name)
    if len(baby_info)>0:
        return baby_info[0]
    else:
        b = BabyInfo(name=baby_name)
        b.save()
        return b

def register_sitter(user_id,sitter_name,baby):
    baby_sitter_info = BabySitterInfo(
        user_id=user_id,
        name=sitter_name,
        baby=baby
    )
    baby_sitter_info.save()