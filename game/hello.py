from entities import Keyboard, Button
from interaction import Interaction

__all__ = ['Hello']

class Hello(Interaction):
    def keyboard(self):
        return Keyboard([[
            Button(self.get_text('button_ru'), lambda: self.set_language('ru')),
        ], [
            Button(self.get_text('button_en'), lambda: self.set_language('en')),
        ]])

    def set_language(self, lang):
        self.context.language = lang
        return 'language_selected'
