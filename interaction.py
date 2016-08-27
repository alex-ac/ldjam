import yaml
import os

from entities import Keyboard, Button

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
        if cmd == 'set_language':
            context.language = args[0]
        if cmd == 'reset':
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
