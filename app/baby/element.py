


from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)

menu_btn = TemplateSendMessage(
    alt_text="Buttons template",
    template=ButtonsTemplate(
        title="功能選單",
        text="請選擇",
        actions=[
            PostbackTemplateAction(
                label='登記',
                text='Menu!Log',
                data='A&登記'
            ),
            PostbackTemplateAction(
                label='補登',
                text='Menu!Log_History',
                data='A&補登'
            ),
            PostbackTemplateAction(
                label="查詢",
                text="Menu!Query",
                data="A&查詢"
            ),
            PostbackTemplateAction(
                label="提醒設定",
                text="Menu!Reimder_Type",
                data="A&提醒設定"
            )
        ]
    )
)



query_btn = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='查詢項目',
        text='請選擇',
        actions=[
            PostbackTemplateAction(
                label="詳細紀錄",
                text="Menu!Query_Type_ALL",
                data="A&詳細紀錄"
            ),
            PostbackTemplateAction(
                label="統計紀錄",
                text="Menu!Query_Type_SUM",
                data="A&統計紀錄"
            ),
            PostbackTemplateAction(
                label="下次進食時間",
                text="Query_Next!Feed~~",
                data="A&下次進食時間"
            ),
        ]
    )
)

log_btn = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='登記選單',
        text='請選擇',
        actions=[
            PostbackTemplateAction(
                label='奶',
                text='Log!Milk**',
                data='A&奶'
            ),
            PostbackTemplateAction(
                label='大便',
                text='Log!Daiper2**',
                data='A&大便'
            ),
            PostbackTemplateAction(
                label='小便',
                text='Log!Daiper1**',
                data='A&小便'
            ),
            PostbackTemplateAction(
                label='體重或體溫',
                text='Menu!Log_WT',
                data='A&體重或體溫'
            )
        ]
    )
)

log_history_btn = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='登記選單',
        text='請選擇',
        actions=[
            PostbackTemplateAction(
                label='奶',
                text='Log!Milk***',
                data='A&奶'
            ),
            PostbackTemplateAction(
                label='大便',
                text='Log!Daiper2***',
                data='A&大便'
            ),
            PostbackTemplateAction(
                label='小便',
                text='Log!Daiper1***',
                data='A&小便'
            ),
            PostbackTemplateAction(
                label='體重或體溫',
                text='Menu!Log_History_WT',
                data='A&體重或體溫'
            )
        ]
    )
)
log_history_btn2 = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='紀錄項目',
        text='請選擇紀錄項目',
        actions=[
            PostbackTemplateAction(
                label='體重',
                text='Log!Weight***',
                data='A&體重'
            ),
            PostbackTemplateAction(
                label='體溫',
                text='Log!Temperature***',
                data='A&體溫'
            )
        ]
    )
)
log_btn2 = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='紀錄項目',
        text='請選擇紀錄項目',
        actions=[
            PostbackTemplateAction(
                label='體重',
                text='Log!Weight**',
                data='A&體重'
            ),
            PostbackTemplateAction(
                label='體溫',
                text='Log!Temperature**',
                data='A&體溫'
            )
        ]
    )
)

query_type_sum_btn = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='查詢寶寶紀錄',
        text='請選擇查詢項目',
        actions=[
            PostbackTemplateAction(
                label='進食與尿布',
                text='Query_SUM!Feed&Daiper@@',
                data='A&進食與尿布'
            )
        ]
    )
)

query_type_all_btn = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='查詢寶寶紀錄',
        text='請選擇查詢項目',
        actions=[
            PostbackTemplateAction(
                label='進食與尿布',
                text='Query_ALL!Feed&Daiper@@',
                data='A&進食與尿布'
            ),
            PostbackTemplateAction(
                label='體重與體溫',
                text='Query_ALL!Weight&Temperature@@',
                data='A&體重與體溫'
            ),
        ]
    )
)


day_btn = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='查詢寶寶紀錄',
        text='請選擇查詢時間',
        actions=[
            PostbackTemplateAction(
                label='今日',
                text='1',
                data='A&今日'
            ),
            PostbackTemplateAction(
                label='一週',
                text='7',
                data='A&一週'
            ),
            PostbackTemplateAction(
                label='一個月',
                text='30',
                data='A&一個月'
            ),
            PostbackTemplateAction(
                label='三個月',
                text='90',
                data='A&三個月'
            )
        ]
    )
)

reminder_btn = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='提醒設定',
        text='選擇',
        actions=[
            PostbackTemplateAction(
                label='設定提醒餵奶',
                text='Reminder!Feed$$',
                data='A&設定提醒餵奶'
            ),
            PostbackTemplateAction(
                label='設定提醒換尿布',
                text='Reminder!Daiper$$',
                data='A&設定提醒換尿布'
            ),
            PostbackTemplateAction(
                label='取消提醒餵奶',
                text='Reminder!Feed$$-1',
                data='A&取消提醒餵奶'
            ),
            PostbackTemplateAction(
                label='取消提醒換尿布',
                text='Reminder!Daiper$$-1',
                data='A&取消提醒換尿布'
            )
        ]
    )
)