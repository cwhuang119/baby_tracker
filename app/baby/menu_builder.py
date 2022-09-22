

from baby.element_map import BABYCUSTOM_BTN
from baby.element_map import SUGGESTIONS_BTN
from baby.element_map import MENU_BTN
from baby.element_map import REMINDER_BTN
from baby.element_map import QUERY_ALL_BTN
from baby.element_map import QUERY_SUM_BTN
from baby.element_map import LOG_BTN
from baby.element_map import PERIOD_BTN
from baby.element_map import LOGHISTORY_BTN


def custon_btn(title='',text='',action_data=[]):
    return {
        'title':title,
        'text':text,
        'action_data':action_data
    }


def build_menu(request_types):
    request_type=request_types[0]
    if request_type=='All':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                MENU_BTN['LogType'],
                MENU_BTN['QueryType'],
                MENU_BTN['Settings'],
                MENU_BTN['Suggestions']
            ]
        }

    elif request_type=='LogType':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                MENU_BTN['Log'],
                MENU_BTN['LogHistory'],
            ]
        }
    elif request_type=='QueryType':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                MENU_BTN['QueryTypeAll'],
                MENU_BTN['QueryTypeSum'],
            ]
        }
    elif request_type=='Suggestions':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                SUGGESTIONS_BTN['NextFeed'],
                SUGGESTIONS_BTN['FeedVolume'],
                SUGGESTIONS_BTN['SleepingTime']
            ]
        }
    elif request_type=='Settings':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                MENU_BTN['BabyCustoms'],
            ]
        }
    elif request_type=='BabyCustoms':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                BABYCUSTOM_BTN['Birthday'],
                BABYCUSTOM_BTN['Gender'],
                BABYCUSTOM_BTN['FeedInterval'],
                BABYCUSTOM_BTN['FeedFrequency']
            ]
        }
    elif request_type=='ReminderType':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                REMINDER_BTN['Feed'],
                REMINDER_BTN['Daiper'],
                REMINDER_BTN['CancelFeed'],
                REMINDER_BTN['CancelDaiper']
            ]
        }
    elif request_type=='QueryTypeAll':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                QUERY_ALL_BTN['Feed&Daiper'],
                QUERY_ALL_BTN['Weight&Temperature'],
                QUERY_ALL_BTN['Height&HeadLength'],
            ]
        }
    elif request_type=='QueryTypeSum':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                QUERY_SUM_BTN['Feed&Daiper'],
            ]
        }
    elif request_type=='Log':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                LOG_BTN['Feed'],
                LOG_BTN['Daiper1'],
                LOG_BTN['Daiper2'],
                MENU_BTN['LogOther'],
            ]
        }
    elif request_type=='LogOther':
                menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                LOG_BTN['Weight'],
                LOG_BTN['Height'],
                LOG_BTN['Temperature'],
                LOG_BTN['HeadLength'],
            ]
        }
    
    elif request_type=='LogHistory':
        menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                LOGHISTORY_BTN['Feed'],
                LOGHISTORY_BTN['Daiper1'],
                LOGHISTORY_BTN['Daiper2'],
                MENU_BTN['LogHistoryOther'],
            ]
        }

    elif request_type=='LogHistoryOther':
                menu_content = {
            "title":"功能選單",
            "text":"請選擇",
            "actions_data":[
                LOGHISTORY_BTN['Weight'],
                LOGHISTORY_BTN['Height'],
                LOGHISTORY_BTN['Temperature'],
                LOGHISTORY_BTN['HeadLength'],
            ]
        }

    elif request_type=='SelectPeriod':
        menu_content = {
            "title":"選擇日期",
            "text":"請選擇",
            "actions_data":[
                PERIOD_BTN['1'],
                PERIOD_BTN['7'],
                PERIOD_BTN['30'],
                PERIOD_BTN['90'],

            ]
        }
    else:
        raise KeyError(f"Invalid request_type:{request_type}")

    return menu_content