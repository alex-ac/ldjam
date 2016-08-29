from entities import Keyboard, Button
from interaction import Interaction

__all__ = ['LanguageSelected']

class LanguageSelected(Interaction):
    def keyboard(self):
        return Keyboard([[
            Button(self.get_text('button'), lambda:'intro')
        ]])
