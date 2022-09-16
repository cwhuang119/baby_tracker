from unittest import TestCase

from baby.dailogflow import MessageParser,DailogController

from baby.models import BabyInfo,BabySitterInfo,Feed

class DailogFlowTestCase(TestCase):

    def setUp(self):
        
        self.user_id = 'test_user_id'
        if len(BabyInfo.objects.filter(name='baby'))==0:
            BabyInfo.objects.create(name='baby')
            baby = BabyInfo.objects.get(name='baby')
            BabySitterInfo.objects.create(name='test',user_id=self.user_id,baby=baby)
        self.log_message = ['123123123','Menu!!LogType','Menu!!Log','Log11Feed**','100']
        self.check_log = ['123123123','Menu!!QueryType','QueryAll!!Feed**','1']
    def test_cache(self):

        dailog_controller = DailogController()
        msg1 = 'Test!!test'
        return_data = dailog_controller.process(msg1,self.user_id)
        self.assertEqual(return_data,{'type': 'text', 'content': 'test', 'follow_up': True})
        self.assertEqual(msg1,dailog_controller.get_last_msg(self.user_id))

        msg2='123123'
        return_data = dailog_controller.process(msg2,self.user_id)
        self.assertEqual(return_data,{'type': 'text', 'content': 'test', 'follow_up': True})
        self.assertEqual(msg1+msg2,dailog_controller.get_last_msg(self.user_id))

        msg3 = 'Test!!123123'
        return_data = dailog_controller.process(msg3,self.user_id)
        self.assertEqual(return_data['type'],'button')
        self.assertEqual('',dailog_controller.get_last_msg(self.user_id))

    def test_log_flow(self):
        dailog_controller = DailogController()
        for msg in self.log_message:
            return_data = dailog_controller.process(msg,self.user_id)
        for msg in self.check_log:
            return_data = dailog_controller.process(msg,self.user_id)



class MessageParserTestCase(TestCase):
    
    def setUp(self):
        self.test_data_array = [
            {
                'message':'123',
                'action':'Menu',
                'request_content':'All',
                'request_types':['All'],
                'request_data':'',
                'request_time':''
            },
            {
                'message':'Menu!!Log',
                'action':'Menu',
                'request_content':'Log',
                'request_types':['Log'],
                'request_data':'',
                'request_time':''
            },
            #action without data and time
            {
                'message':'Log!!Daiper**',
                'action':'Log',
                'request_content':'Daiper**',
                'request_types':['Daiper'],
                'request_data':'',
                'request_time':''
            },
            #action with data but without time
            {
                'message':'Log!!Daiper**1',
                'action':'Log',
                'request_content':'Daiper**1',
                'request_types':['Daiper'],
                'request_data':'1',
                'request_time':''
            },
            #action with data but without time
            {
                'message':'Log!!Daiper**1@@',
                'action':'Log',
                'request_content':'Daiper**1@@',
                'request_types':['Daiper'],
                'request_data':'1',
                'request_time':''
            },
            #action with data but without time
            {
                'message':'Log!!Daiper**1@@202208081010',
                'action':'Log',
                'request_content':'Daiper**1@@202208081010',
                'request_types':['Daiper'],
                'request_data':'1',
                'request_time':'202208081010'
            },
            #multiple request types
            {
                'message':'QueryAll!!Feed&Daiper**3',
                'action':'QueryAll',
                'request_content':'Feed&Daiper**3',
                'request_types':['Feed','Daiper'],
                'request_data':'3',
                'request_time':''
            },


        ]

    def test_parse(self):

        for test_data in self.test_data_array:
            #test single function
            action,request_content = MessageParser.parse_action(test_data['message'])
            self.assertEqual(action,test_data['action'])
            self.assertEqual(request_content,test_data['request_content'])
            #test single function
            request_types,request_data,request_time = MessageParser.parse_request_content(request_content)
            self.assertEqual(request_types,test_data['request_types'])
            self.assertEqual(request_data,test_data['request_data'])
            self.assertEqual(request_time,test_data['request_time'])
            #test integrated function
            action,request_types,request_data,request_time = MessageParser.parse(test_data['message'])
            self.assertEqual(action,test_data['action'])
            self.assertEqual(request_types,test_data['request_types'])
            self.assertEqual(request_data,test_data['request_data'])
            self.assertEqual(request_time,test_data['request_time'])
