from django.conf import settings

from baby.line_api import LineBot
from baby.reminder import Reminder
from baby.dailogflow import DailogController
linebot = LineBot(settings.LINE_CHANNEL_ACCESS_TOKEN,settings.LINE_CHANNEL_SECRET)
reminder = Reminder(linebot)

dailog_controller = DailogController()