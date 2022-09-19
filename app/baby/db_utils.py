

import datetime
import time

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
        raise KeyError(f"User ID not found:{user_id}")

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