#!/usr/bin/env python3

import sys
import yaml
import logging
import requests
import os

from datetime import datetime
from argparse import ArgumentParser

class Config(object):
    def __init__(self, telegram={}, log={}, storage={}):
        self.telegram_token = telegram.get('token')
        self.log_level = log.get('level', 'WARNING')
        self.storage_file = storage.get('file', 'data.yaml')

    @classmethod
    def load(cls, data):
        parsed_data = yaml.load(data)
        return Config(**parsed_data)

    def save(self):
        return yaml.dump({
            'telegram': {
                'token': self.telegram_token,
            },
            'log': {
                'level': self.log_level,
            },
            'storage': {
                'file': self.storage_file,
            }
        })

class Button(object):
    def __init__(self, text):
        self.text = text

class Keyboard(object):
    def __init__(self, *buttons):
        self.buttons = buttons

    def as_dict(self):
        return {
            'one_time_keyboard': True,
            'resize_keyboard': True,
            'keyboard': [[
              { 'text': button.text }
              for button in row
            ] for row in self.buttons ],
        }

class Storage(object):
    def __init__(self, last_update_id=None):
        self.last_update_id = None
    
    @classmethod
    def load(cls, data):
        return cls(**yaml.load(data))

    def save(self):
        return yaml.dump({
            'last_update_id': self.last_update_id,
        })

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

    def __repr__(self):
        return '<Message id={} from={} text={}>'.format(self.message_id, self.from_user, self.text)


class Update(object):
    def __init__(self, update_id, message=None, **kwargs):
        self.update_id = update_id
        self.message = Message(**message)

    def __repr__(self):
        return '<Update id={} message={}>'.format(self.update_id, repr(self.message))


class Interaction(object):
    def __init__(self, text={}, keyboard={}, fallback={}, next=None):
        self.text = text
        self.keyboard = keyboard
        self.fallback = fallback
        self.next = next

    @classmethod
    def load(cls, name):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game', name + '.yaml')) as f:
            return cls(**yaml.load(f.read()))

    def resolve_text(self, language, value):
        if language is None:
            if isinstance(value, dict):
                return '\n'.join(t for t in value.values())
            elif isinstance(value, str):
                return value
            else:
                return '<couldnotloadtext>'
        else:
            if isinstance(value, dict):
                return value.get(language, '<couldnotloadtext>')
            elif isinstance(self.text, str):
                return value
            else:
                return '<couldnotloadtext>'

    def process_cmd(self, context, cmd, *args):
        logging.debug('command %s', cmd)
        if cmd == 'set_language':
            logging.debug('set_language %s', args[0])
            context.language = args[0]
        if cmd == 'reset':
            logging.debug('reset')
            context.reset()

    def run(self, context, bot):
        keyboard=Keyboard([
            Button(self.resolve_text(context.language, button.get('label')))
            for button in self.keyboard])
        bot.send(
            context.chat,
            self.resolve_text(context.language, self.text),
            keyboard=keyboard)

        ok = False
        while not ok:
            reply = yield
            for button in self.keyboard:
                if reply.text == self.resolve_text(context.language, button.get('label')):
                    ok = True
                    cmd = button.get('cmd')
                    if cmd:
                        self.process_cmd(context, *cmd)
                    break
            if not ok:
                bot.send(
                    context.chat,
                    self.resolve_text(context.language, self.fallback),
                    keyboard=keyboard)

        yield self.next

class Context(object):
    def __init__(self, chat):
        self.chat = chat
        self.reset()

    def reset(self):
        self.language = None

class Bot(object):
    URL_MASK = 'https://api.telegram.org/bot{token}/{method}'
    def __init__(self, token, storage):
        self.token = token
        self.storage = storage
        self.session = requests.Session()
        self.chats = {}
        self.contexts = {}

    def request(self, method, params=None):
        url = self.URL_MASK.format(token=self.token, method=method)
        if params is None:
            logging.debug('GET %s', url)
            response = self.session.get(url)
        else:
            logging.debug('POST %s %s', url, params)
            response = self.session.post(url, json=params)
        logging.debug('> %d', response.status_code)
        if response.status_code != 200:
            print(response.json())
            return
        message = response.json()
        if not message.get('ok', False):
            logging.warning('> !ok: %s', message.get('error_code', 'empty error code'))
            print(response.json())
            return

        return message.get('result', None)

    def get_updates(self, last_id):
        params = {
            'timeout': 3600,
        }
        if last_id is not None:
            params.update({'offset': last_id+1})
        updates = self.request('getUpdates', params=params)
        if updates is not None:
            if not isinstance(updates, list):
                logging.error('list expected but `%s` met.', updates)
                return

            return [Update(**update) for update in updates]

    def send(self, chat, text, reply_to=None, keyboard=None):
        params = {
          'chat_id': chat.id,
          'text': text,
        }
        if reply_to is not None:
            params.update({'reply_to_message_id': reply_to.message_id})
        if keyboard is not None:
            params.update({'reply_markup': keyboard.as_dict()})
        message = self.request('sendMessage', params=params)
        if message is not None:
            return Message(**message)

    def wait_message(self, chat):
        yield

    def process(self, chat, next_interaction):
        while next_interaction is not None:
            self.chats[chat.id] = Interaction.load(next_interaction).run(
                self.contexts[chat.id], self)
            next_interaction = next(self.chats[chat.id])

    def run(self):
        while True:
            logging.debug(self.storage.last_update_id)
            for update in self.get_updates(self.storage.last_update_id):
                if not self.storage.last_update_id or self.storage.last_update_id < update.update_id:
                    self.storage.last_update_id = update.update_id
                if not update.message:
                    logging.debug('There are no message, skipping update')
                    continue
                message = update.message

                if message.chat.id in self.chats:
                    self.process(message.chat, self.chats[message.chat.id].send(message))
                else:
                    self.contexts[message.chat.id] = Context(message.chat)
                    self.process(message.chat, 'hello')

def parse_args(argv=None):
    parser = ArgumentParser(description='Run game bot.')
    parser.add_argument('--config', '-c',
                        default='bot.yaml',
                        help='Configuration file.')
    parser.add_argument('--write-default',
                        default=False,
                        action='store_true',
                        help='Write default cofig file.')
    parser.add_argument('--log-level',
                        default=None,
                        help='Specify log level.')
    return parser.parse_args(argv)

def run(argv=None):
    args = parse_args(argv)

    if args.write_default:
        with open(args.config, 'w') as f:
            f.write(Config().save())
        return

    with open(args.config) as f:
        config = Config.load(f.read())

    if args.log_level:
        config.log_level = log_level

    logging.basicConfig(level=config.log_level)

    try:
        with open(config.storage_file) as f:
            storage = Storage.load(f.read())
    except IOError:
        storage = Storage()

    try:
        Bot(config.telegram_token, storage).run()
    except:
        with open(config.storage_file, 'w') as f:
            f.write(storage.save())
        raise

if __name__ == '__main__':
    sys.exit(run())
