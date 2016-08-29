import os

import yaml

class Item(object):
    def __init__(self, name, description, in_hands_text):
        self.name = name
        self.description = description
        self.in_hands_text = in_hands_text

    @classmethod
    def load(cls, name):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                  'game', 'items', name + '.yaml')) as f:
            return cls(**yaml.load(f.read()))
