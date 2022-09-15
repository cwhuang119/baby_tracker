from baby.menu_builder import build_menu
from baby.element_map import ParseConfig

class DailogController:
    def __init__(self):
        self.cache={}
    def get_last_msg(self,user_id:str):
        return self.cache.get(user_id) or ''
    def process(self,message:str,user_id:str,followup:bool):
        #check if follow up exists and concate last msg
        if followup:
            last_message = self.get_last_msg(user_id)
            message=last_message+message
        #parse message get action and request data
        action,request_types,request_data = self.parse_msg(message)

        #execute action

        #gen return data
        if action=='Menu':
            data = build_menu(request_types,request_data)
        #format return data
        return data

    def parse_msg(self,message:str):
        return MessageParser.parse(message)



class MessageParser:

    @classmethod
    def parse_action(cls,message:str):
        if '!' in message:
            action,request_content = message.split(ParseConfig['action_parser'])
        else:
            action='Menu'
            request_content='All'
        return action,request_content

    @classmethod
    def parse(cls,message:str):
        action,request_content = cls.parse_action(message)
        request_types,request_data = cls.parse_request_content(request_content)
        return action,request_types,request_data

    @classmethod
    def parse_request_content(cls,request_content:str):
        #follow with content
        if '**' in request_content:
            request_types,request_data = request_content.split('**')
        else:
            request_types=request_content
            request_data=''
        request_types = request_types.split('&')
        return request_types,request_data



