from datetime import datetime

class Chat(object):
    def __init__(self, id, type, title=None, username=None, first_name=None, last_name=None):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

class User(object):
    def __init__(self, id, first_name, last_name=None, username=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

class MessageEntity(object):
    def __init__(self, type, offset, length, **kwargs):
        self.type = type
        self.offset = offset
        self.length = length

class Message(object):
    def __init__(self, message_id, date, chat, text=None, entities=[], **kwargs):
        self.message_id = message_id
        self.from_user = kwargs.get('from')
        self.text = text
        self.date = datetime.fromtimestamp(date)
        self.chat = Chat(**chat)
        self.entities = [MessageEntity(**entity) for entity in entities]


class Update(object):
    def __init__(self, update_id, message=None, **kwargs):
        self.update_id = update_id
        self.message = Message(**message)

class Keyboard(object):
    def __init__(self, buttons):
        self.buttons = buttons

    def as_dict(self):
        return {
            'keyboard': [[{'text': button.text}] for button in self.buttons],
            'resize_keyboard': True,
            'one_time_keyboard': True,
        }

class Button(object):
    def __init__(self, text):
        self.text = text
