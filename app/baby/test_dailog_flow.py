from unittest import TestCase

from baby.dailogflow import MessageParser

class DailogFlowTestCase(TestCase):

    def setUp(self):
        pass

    def test_1(self):
        pass

class MessageParserTestCase(TestCase):
    
    def setUp(self):
        pass

    def test_parse_action(self):

        action,request_content = MessageParser.parse_action('Menu!Log')
        self.assertEqual(action,'Menu')
        self.assertEqual(request_content,'Log')

        action,request_content = MessageParser.parse_action('123')
        self.assertEqual(action,'Menu')
        self.assertEqual(request_content,'All')

        action,request_content = MessageParser.parse_action('Log!Daiper1**@202208081010')
        self.assertEqual(action,'Log')
        self.assertEqual(request_content,'Daiper1**@202208081010')


    def test_parsing_menu(self):

        action,request_types,request_data = MessageParser.parse('Menu!Log')
        self.assertEqual(action,'Menu')
        self.assertEqual(request_types,['Log'])
        self.assertEqual(request_data,'')

        #if not recognize message will send back Menu!All
        action,request_types,request_data = MessageParser.parse('123222')
        self.assertEqual(action,'Menu')
        self.assertEqual(request_types,['All'])
        self.assertEqual(request_data,'')

    def test_parsing_log(self):
        pass
