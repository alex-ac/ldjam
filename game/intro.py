__all__ = [ 'Intro' ]

from map import Map
from entities import Keyboard, Button
from interaction import Interaction

class Intro(Interaction):
    def on_start(self):
        self.context.inventory = None
        self.context.item_in_hands = None
        self.context.hunger = 0
        self.context.map = Map()
        self.context.location = self.context.map.get(0, 0)

    def keyboard(self):
        return Keyboard([[
            Button(self.get_text('continue'), lambda:'gameplay')
        ]])
