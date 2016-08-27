import requests
import logging

from entities import Update, Message
from context import Context
from interaction import Interaction

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


