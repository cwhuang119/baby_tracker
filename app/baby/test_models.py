from django.test import TestCase

import datetime
import time

# Create your tests here.
from baby.models import BabyInfo,BabySitterInfo
from baby.models import Feed,Weight,Daiper,Height,HeadLength,Temperature

class BabyInfoTestCase(TestCase):
    def setUp(self):
        BabyInfo.objects.create(name="baby1")
        BabyInfo.objects.create(name="baby2",birthday="2022-08-06",gender='male')

    def test_babyinfo(self):
        """Animals that can speak are correctly identified"""
        baby1 = BabyInfo.objects.get(name="baby1")
        baby2 = BabyInfo.objects.get(name="baby2")
        self.assertEqual(baby1.name,'baby1')
        self.assertEqual(baby1.birthday,datetime.date.today())
        self.assertEqual(baby1.gender,'')
        self.assertEqual(baby2.birthday, datetime.date(2022,8,6))


class BabyActivityTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        baby1 = BabyInfo.objects.create(name="baby1")
        sitter = BabySitterInfo.objects.create(
            baby=baby1,
            name='sitter1',
            user_id='sitter1_user_id'
            )

        #set up feed data
        time_stamp = 1663052300.895308
        volume = 10
        Feed.objects.create(
            baby=baby1,
            sitter=sitter,
            time_stamp=time_stamp,
            volume=volume
        )

        #setup daiper data
        time_stamp = 1663052400.895308
        Daiper.objects.create(
            baby=baby1,
            sitter=sitter,
            time_stamp=time_stamp,
            change_type='Daiper1'
        )
        time_stamp = 1663052500.895308
        Daiper.objects.create(
            baby=baby1,
            sitter=sitter,
            time_stamp=time_stamp,
            change_type='Daiper2'
        )
        #setup weight data
        
        #setup height data

        #setup head length data

        #setup temperature data

    def test_feed(self):
        baby1 = BabyInfo.objects.get(name="baby1")
        feeds = Feed.objects.filter(baby=baby1)
        self.assertEqual(len(feeds),1)
        self.assertEqual(feeds[0].volume,10)



    def test_daiper(self):
        baby1 = BabyInfo.objects.get(name="baby1")
        daipers = Daiper.objects.filter(baby=baby1).order_by('time_stamp')
        self.assertEqual(len(daipers),2)
        self.assertEqual(daipers[0].change_type,'Daiper1')
        self.assertEqual(daipers[1].change_type,'Daiper2')
