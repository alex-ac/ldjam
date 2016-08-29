import os

import yaml

from item import Item

class Location(object):
    def __init__(self, description, weight, items=[]):
        self.description = description
        self.weight = weight
        self.items = [Item.load(item) for item in items]

    @classmethod
    def load(cls, name):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                  'game', 'locations', name + '.yaml')) as f:
            return cls(**yaml.load(f.read()))
