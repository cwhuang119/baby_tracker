
from urllib import request
from baby.menu_builder import build_menu
from abc import abstractclassmethod
import time

from baby.db_utils import log_data


def action_factory(action_type):
    return eval(f'{action_type}Action()')

class Action:

    
    def gen_return_data(self,content_type,content,follow_up):
        return {
            'type':content_type,
            'content':content,
            'follow_up':follow_up
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
    
    def gen_success_data(self,baby,sitter,request_type,request_data):
        msg = f"{sitter.name}紀錄{baby.name}"
        if request_type=='Daiper':
            change_type = '小便' if request_data=='1' else '大便'
            msg+=f"{change_type}一次"
        else:
            msg+=f"{self.success_lines[request_type][0]}{request_data}{self.success_lines[request_type][1]}"
        return msg

    def gen_follow_up_data(self,request_type):
        return self.follow_up_lines[request_type]

    def gen_return_lines(self,follow_up,baby,sitter,request_type,request_data):
        if follow_up:
            return self.gen_follow_up_data(request_type)
        else:
            return self.gen_success_data(baby,sitter,request_type,request_data)

    def execute(self,baby,sitter,request_types,request_data,request_time):
        
        request_type = request_types[0]
        if request_data == '':
            follow_up = True
        else:
            follow_up = False
            request_time = self.get_current_timestamp()
            log_data(baby,sitter,request_types[0],request_data,request_time)

        content = self.gen_return_lines(
            follow_up,
            baby,
            sitter,
            request_type,
            request_data
        )
        return self.gen_return_data('text',content,follow_up)