
from baby.menu_builder import build_menu
from abc import abstractclassmethod

def action_factory(action_type,request_types,request_data,request_time):
    return eval(f'{action_type}Action(request_types,request_data,request_time)')

class Action:
    def __init__(self,request_types:list,request_data:str,request_time:str):

        self.request_types = request_types
        self.request_data = request_data
        self.request_time = request_time

    @abstractclassmethod
    def gen_return_data(self):
        pass

    @abstractclassmethod
    def execute(self):
        pass

class MenuAction(Action):

    def gen_return_data(self):
        return build_menu(self.request_types)

    def execute(self):
        follow_up=False
        return self.gen_return_data(),follow_up

class LogAction(Action):
    
    def gen_return_data(self):
        pass

    def excute(self):
        pass