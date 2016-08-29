import yaml
import sys
import os
import importlib
import itertools
from traceback import print_exc

from jinja2 import Template, Environment

from entities import Keyboard, Button

class Interaction(object):
    def __init__(self, context, bot, name):
        self.name = name
        self.context = context
        self.bot = bot

        self.env = Environment()
        self.env.filters['localize'] = lambda text:self.get_text(text)

        with open(self.resolve_path(self.name + '.yaml')) as f:
            self.l10n = yaml.safe_load(f.read())

    @classmethod
    def resolve_path(cls, path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game', path)

    @classmethod
    def load(cls, context, bot, name):
        try:
            module = importlib.import_module('game.' + name)
            module = importlib.reload(module)
            cls_name = next(iter(module.__all__))
            cls = getattr(module, cls_name)
            return cls(context, bot, name)
        except:
            print_exc()

    def get_text(self, key):
        text = ''
        value = self.l10n.get(key, '')

        if self.context.language is None:
            if isinstance(value, dict):
                text = '\n'.join(t for t in value.values())
            elif isinstance(value, str):
                text = value
            else:
                text = str(value)
        elif isinstance(value, dict):
            text = value.get(self.context.language)
            if text is None:
                text = next(value.values())
        elif isinstance(value, str):
            text = value

        try:
            return self.env.from_string(text).render(**self.context.as_dict())
        except:
            print_exc()
            return ''

    def on_start(self):
        pass

    def text(self):
        return self.get_text('text')

    def fallback(self):
        return self.get_text('fallback')

    def keyboard(self):
        return Keyboard([[]])
 
    def run(self):
        self.bot.send(
            self.context.chat,
            self.text(),
            keyboard=self.keyboard())

    def on_message(self, reply):
        for button in itertools.chain(*self.keyboard().buttons):
            if reply.text == button.text:
                return button.on_click()

        self.bot.send(
            self.context.chat,
            self.fallback(),
            keyboard=self.keyboard())

    def on_finish(self):
        pass
