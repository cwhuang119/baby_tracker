from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)


def build_line_element(data):
    if data['type']=='text':
        return LineTextMessage.build(data['content'])
    elif data['type']=='button':
        return LineButton.build(data['content'])



class LineTextMessage:
    
    @classmethod
    def build(cls,text_data):
        return TextSendMessage(text_data)


class LineButton:
    
    @classmethod
    def build(cls,button_data):
        template = ButtonsTemplate(
            title=button_data['title'],
            text=button_data['text'],
            actions=cls._build_actions(button_data['actions_data'])
        )
        alt_text = 'Buttons template'
        return cls._build_template(template,alt_text)
    @classmethod
    def _build_template(cls,template,alt_text):
        return TemplateSendMessage(
            alt_text=alt_text,
            template=template
        )
    @classmethod
    def _build_actions(cls,actions_data):
        actions = []
        for action_data in actions_data:
            actions.append(cls._build_action(action_data))
        return actions
    @classmethod
    def _build_action(cls,action_data):
        return PostbackTemplateAction(
            label=action_data['label'],
            text=action_data['text'],
            data=action_data['data']
        )