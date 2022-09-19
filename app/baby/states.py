from django.conf import settings

from baby.line_api import LineBot
from baby.dailogflow import DailogController
linebot = LineBot(settings.LINE_CHANNEL_ACCESS_TOKEN,settings.LINE_CHANNEL_SECRET)

dailog_controller = DailogController()