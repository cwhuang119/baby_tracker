
from abc import abstractclassmethod
import time
import datetime

from baby.db_utils import set_babycustoms,get_baby_customs
from baby.db_utils import log_data,query_log,get_last_weight,get_last_feed
from baby.format_return_data import format_query_all_content,format_query_sum_content,gen_lines_babycustoms
from baby.format_return_data import gen_lines_Log,gen_line_ask_time,gen_line_log_failed,gen_lines_suggestions
from baby.menu_builder import build_menu

def action_factory(action_type):
    try:
        return eval(f'{action_type}Action()')
    except NameError:
        return ErrorAction()

class Action:

    def gen_return_data(self,content_type,content,follow_up,follow_up_parser=''):
        return {
            'type':content_type,
            'content':content,
            'follow_up':follow_up,
            'follow_up_parser':follow_up_parser
        }

    @abstractclassmethod
    def execute(self,baby,sitter,request_types,request_data,request_time):
        """
        return_data:
            type:text/btn
            content:
        
        """
        pass
    
    def get_current_timestamp(self):
        return time.time()

    def format_time_stamp(self,time_stamp,time_format):
        return datetime.datetime.fromtimestamp(time_stamp).strftime(time_format)

    def convert_time_str_2_timestamp(self,time_str,time_format="%Y%m%d%H%M"):
        return time.mktime(datetime.datetime.strptime(time_str,time_format).timetuple())

class ErrorAction(Action):
    def execute(self,baby,sitter,request_types,request_data,request_time):
        return self.gen_return_data('text','Invalid Action',False)

class TestAction(Action):
    def execute(self,baby,sitter,request_types,request_data,request_time):
        
        return self.gen_return_data('text','test',True)
class Test2Action(Action):
    def execute(self,baby,sitter,request_types,request_data,request_time):
        
        return self.gen_return_data('text','test2',False)


class MenuAction(Action):

    def execute(self,baby,sitter,request_types,request_data,request_time):
        follow_up=False
        menu = build_menu(request_types)
        return self.gen_return_data('button',menu,follow_up)



class LogAction(Action):

    def execute(self,baby,sitter,request_types,request_data,request_time):

        request_type = request_types[0]
        if request_data == '':
            follow_up = True
            content = gen_lines_Log(baby,sitter,request_type,request_data,follow_up)
        else:
            follow_up = False
            request_time = self.get_current_timestamp()
            try:
                success = log_data(baby,sitter,request_types[0],request_time,request_data)
                if success:
                    content = gen_lines_Log(baby,sitter,request_type,request_data,follow_up)
                else:
                    content = gen_line_log_failed()
            except:
                content = gen_line_log_failed()

        return self.gen_return_data('text',content,follow_up)


class LogHistoryAction(Action):

    def execute(self,baby,sitter,request_types,request_data,request_time):
        request_type = request_types[0]
        if request_data=='':
            follow_up = True
            content = gen_lines_Log(baby,sitter,request_type,request_data,follow_up)
            follow_up_parser = ''
        elif request_time=='':
            follow_up = True
            content = gen_line_ask_time()
            follow_up_parser = '@@'
        else:
            try:
                follow_up = False
                request_time_stamp = self.convert_time_str_2_timestamp(request_time)
                log_data(baby,sitter,request_types[0],request_time_stamp,request_data)
                follow_up_parser = ''
                content = gen_lines_Log(baby,sitter,request_type,request_data,follow_up)
            except:
                follow_up = False
                follow_up_parser = ''
                content = gen_line_log_failed()

        return self.gen_return_data('text',content,follow_up,follow_up_parser)

class QueryAllAction(Action):

    def execute(self,baby,sitter,request_types,request_data,request_time):
        if request_data=='':
            follow_up = True
            content = build_menu(['SelectPeriod'])
            content_type = 'button'
        else:
            follow_up = False
            query_content = query_log(baby=baby,query_types=request_types,period=request_data)
            content_type = 'text'
            content = format_query_all_content(query_content,baby)
        return self.gen_return_data(content_type,content,follow_up)




class QuerySumAction(Action):
    def execute(self,baby,sitter,request_types,request_data,request_time):
        if request_data=='':
            follow_up = True
            content = build_menu(['SelectPeriod'])
            content_type = 'button'
        else:
            follow_up = False
            query_content = query_log(baby=baby,query_types=request_types,period=request_data)
            content_type = 'text'
            content = format_query_sum_content(query_content,baby)
        return self.gen_return_data(content_type,content,follow_up)

class BabyCustomsAction(Action):
    def execute(self,baby,sitter,request_types,request_data,request_time):
        request_type = request_types[0]
        if request_data=='':
            follow_up = True
            content = gen_lines_babycustoms(baby,sitter,request_type,request_data,follow_up)
            content_type = 'text'
        else:
            follow_up = False
            success = set_babycustoms(baby=baby,sitter=sitter,request_type=request_type,request_data=request_data)
            content_type = 'text'
            content = gen_lines_babycustoms(baby,sitter,request_type,request_data,follow_up)
        return self.gen_return_data(content_type,content,follow_up)


class SuggestionsAction(Action):
    def execute(self,baby,sitter,request_types,request_data,request_time):
        request_type = request_types[0]
        follow_up = False
        content_type = 'text'
    
        baby_customs = get_baby_customs(baby)
        last_feed,last_weight = get_last_feed(baby),get_last_weight(baby)
        content = gen_lines_suggestions(
            baby=baby,
            sitter=sitter,
            request_type=request_type,
            baby_customs=baby_customs,
            last_feed=last_feed,
            last_weight=last_weight
            )


        return self.gen_return_data(content_type,content,follow_up)