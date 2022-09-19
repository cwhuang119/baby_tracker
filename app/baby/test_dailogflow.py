from unittest import TestCase

from baby.dailogflow import MessageParser,DailogController

from baby.models import BabyInfo,BabySitterInfo,Daiper

class DailogFlowTestCase(TestCase):

    def setUp(self):
        
        self.user_id = 'test_user_id'
        if len(BabyInfo.objects.filter(name='baby'))==0:
            BabyInfo.objects.create(name='baby')
            baby = BabyInfo.objects.get(name='baby')
            BabySitterInfo.objects.create(name='test',user_id=self.user_id,baby=baby)
        self.log_message_Feed = ['123123123','Menu!!LogType','Menu!!Log','Log!!Feed**','100']
        self.check_log_Feed = ['123123123','Menu!!QueryType','QueryAll!!Feed**','1']

        self.log_message_Daiper1 = ['123123123','Menu!!LogType','Menu!!Log','Log!!Daiper**1']
        self.check_log_Daiper1 = ['123123123','Menu!!QueryType','QueryAll!!Daiper**','1']

        self.log_message_Daiper2 = ['123123123','Menu!!LogType','Menu!!Log','Log!!Daiper**2']
        self.check_log_Daiper2 = ['123123123','Menu!!QueryType','QueryAll!!Daiper**','1']

    def test_cache(self):

        dailog_controller = DailogController()
        msg1 = 'Test!!test'
        return_data = dailog_controller.process(msg1,self.user_id)
        self.assertEqual(return_data,{'type': 'text', 'content': 'test', 'follow_up': True,'follow_up_parser':''})
        self.assertEqual(msg1,dailog_controller.get_last_msg(self.user_id))

        msg2='123123'
        return_data = dailog_controller.process(msg2,self.user_id)
        self.assertEqual(return_data,{'type': 'text', 'content': 'test', 'follow_up': True,'follow_up_parser':''})
        self.assertEqual(msg1+msg2,dailog_controller.get_last_msg(self.user_id))

        msg3 = 'Test!!123123'
        return_data = dailog_controller.process(msg3,self.user_id)
        self.assertEqual(return_data['type'],'button')
        self.assertEqual('',dailog_controller.get_last_msg(self.user_id))

    def test_log_flow_Feed(self):
        dailog_controller = DailogController()
        #test log flow
        for msg in self.log_message_Feed:
            return_data = dailog_controller.process(msg,self.user_id)
        #get detail log
        for msg in self.check_log_Feed:
            return_data = dailog_controller.process(msg,self.user_id)
        #check log success and can be found in detail logs
        self.assertEqual(True,'100 ml' in return_data['content'])

    def test_log_flow_Daiper1(self):
        dailog_controller = DailogController()
        #test log flow
        for msg in self.log_message_Daiper1:
            return_data = dailog_controller.process(msg,self.user_id)
        #get detail log
        for msg in self.check_log_Daiper1:
            return_data = dailog_controller.process(msg,self.user_id)
        #check log success and can be found in detail logs
        self.assertEqual(True,'小便' in return_data['content'])

    def test_log_flow_Daiper2(self):
        dailog_controller = DailogController()
        #test log flow
        for msg in self.log_message_Daiper2:
            return_data = dailog_controller.process(msg,self.user_id)
        #get detail log
        for msg in self.check_log_Daiper2:
            return_data = dailog_controller.process(msg,self.user_id)
        #check log success and can be found in detail logs
        self.assertEqual(True,'大便' in return_data['content'])


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
