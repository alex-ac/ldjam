import yaml
import sys
import os
import importlib

from jinja2 import Template

from entities import Keyboard, Button

class Interaction(object):
    def __init__(self, text={}, keyboard={}, fallback={}, next=None):
        self.text = text
        self.keyboard = keyboard
        self.fallback = fallback
        self.next = next

    @classmethod
    def resolve_path(cls, path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game', path)

    @classmethod
    def load(cls, name):
        with open(cls.resolve_path(name + '.yaml')) as f:
            return cls(**yaml.load(f.read()))

    def resolve_text(self, context, value):
        text = ''
        if context.language is None:
            if isinstance(value, dict):
                text = '\n'.join(t for t in value.values())
            elif isinstance(value, str):
                text = value
            else:
                text ='<couldnotloadtext>'
        else:
            if isinstance(value, dict):
                text =  value.get(context.language, '<couldnotloadtext>')
            elif isinstance(self.text, str):
                text = value
            else:
                text = '<couldnotloadtext>'
        return Template(text).render(**context.as_dict())

    def process_cmd(self, context, cmd, *args):
        if self.resolve_path('') not in sys.path:
            sys.path.append(self.resolve_path(''))
        module = importlib.import_module(cmd)
        module = importlib.reload(module)
        module.run(context, *args)

    def run(self, context, bot):
        keyboard=Keyboard([
            Button(self.resolve_text(context, button.get('label')))
            for button in self.keyboard])
        bot.send(
            context.chat,
            self.resolve_text(context, self.text),
            keyboard=keyboard)

        ok = False
        while not ok:
            reply = yield
            for button in self.keyboard:
                if reply.text == self.resolve_text(context, button.get('label')):
                    ok = True
                    cmd = button.get('cmd')
                    if cmd:
                        self.process_cmd(context, *cmd)
                    break
            if not ok:
                bot.send(
                    context.chat,
                    self.resolve_text(context, self.fallback),
                    keyboard=keyboard)

        yield self.next
