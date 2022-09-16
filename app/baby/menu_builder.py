

from baby.element_map import BABYCUSTOM_BTN
from baby.element_map import SUGGESTIONS_BTN
from baby.element_map import MENU_BTN
from baby.element_map import REMINDER_BTN
from baby.element_map import QUERY_ALL_BTN
from baby.element_map import QUERY_SUM_BTN
from baby.element_map import LOG_BTN

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
                MENU_BTN['ReminderType'],
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
    else:
        raise KeyError(f"Invalid request_type:{request_type}")

    return menu_content