



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


def log_data(baby,sitter,log_type,time_stamp,value):
    
    eval(f"log_{log_type}(baby,sitter,time_stamp,value)")


def log_Feed(baby,sitter,time_stamp,value):
    feed = Feed(
    baby=baby,
    sitter=sitter,
    time_stamp=time_stamp,
    volume=value
    )
    feed.save()
def log_Daiper(baby,sitter,time_stamp,value):
    daiper = Daiper(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        change_type=value
    )
    daiper.save()

def log_Temperature(baby,sitter,time_stamp,value):
    temperature = Temperature(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        temperature=value
    )
    temperature.save()
def log_Weight(baby,sitter,time_stamp,value):
    weight = Weight(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        weight=value
    )
    weight.save()
def log_Height(baby,sitter,time_stamp,value):
    weight = Height(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        height=value
    )
    weight.save()
def log_HeadLength(baby,sitter,time_stamp,value):
    weight = HeadLength(
        baby=baby,
        sitter=sitter,
        time_stamp=time_stamp,
        head_length=value
    )
    weight.save()