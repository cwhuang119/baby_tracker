from baby.element_map import ParseConfig
from baby.actions import action_factory
class DailogController:
    def __init__(self):
        self.cache={}
        self.follow_up_list = []
    
    def get_last_msg(self,user_id:str):
        return self.cache.get(user_id) or ''

    def process(self,message:str,user_id:str):
        #check if follow up exists and concate last msg
        if user_id in self.follow_up_list:
            last_message = self.get_last_msg(user_id)
            message = last_message+message
        
        #parse message get action and request data
        action_type,request_types,request_data,request_time = self.parse_msg(message)

        action = action_factory(action_type,request_types,request_data,request_time)

        return_data,follow_up = action.execute()

        if follow_up:
            self.follow_up_list.append(user_id)
        else:
            if user_id in self.follow_up_list:
                self.follow_up_list.pop(self.follow_up_list.index(user_id))

        #format return data
        return return_data

    def parse_msg(self,message:str):
        return MessageParser.parse(message)


class MessageParser:

    @classmethod
    def parse_action(cls,message:str):

        if ParseConfig['action_parser'] in message:
            action_type,request_content = message.split(ParseConfig['action_parser'])
        else:
            action_type='Menu'
            request_content='All'
        return action_type,request_content

    @classmethod
    def parse(cls,message:str):
        action_type,request_content = cls.parse_action(message)
        request_types,request_data,request_time = cls.parse_request_content(request_content)
        return action_type,request_types,request_data,request_time

    @classmethod
    def parse_request_content(cls,request_content:str):
        """
        Daiper**1@@202208081010
        {request_types_str}**{request_data}@@{request_time}
        Parsing request content into:
            request_types: 
                type: list
                ex: ['Daiper']
            request_data: 1
                type: str
                ex: 1
            request_time: 
                type: str
                ex: 202208081010
        """
        vp = ParseConfig['value_parser']
        tp = ParseConfig['time_parser']

        # check last two char if equal value_parser or time_parser will need followup questions
        if request_content[-2:] == vp:
            #Daiper** 
            request_types_str = request_content[:-2]
            request_data = ''
            request_time = ''

        elif request_content[-2:] == tp:
            #Daiper**1@@
            request_types_str,request_data = request_content[:-2].split(vp)            
            request_time = ''

        elif vp in request_content and tp not in request_content:
            #Daiper**1
            request_types_str,request_data = request_content.split(vp)
            request_time = ''

        elif vp in request_content and tp in request_content:
            #Daiper**1@202208081010
            request_types_str,request_data = request_content.split(vp)
            request_data,request_time = request_data.split(tp)

        elif vp not in request_content and tp not in request_content:
            #Log
            request_types_str = request_content
            request_data = ''
            request_time = ''
        else:
            raise ValueError(f"Invalid request content:{request_content}")
        
        request_types = request_types_str.split('&') #convert request_types_str to list

        return request_types,request_data,request_time



