import yaml
import os
import random

from location import Location

class Map(object):
    def __init__(self):
        self.matrix = {}

    @classmethod
    def locations(cls):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game', 'locations')

    def random_location(self):
        variants = []
        for location_yaml in os.listdir(self.locations()):
            with open(os.path.join(self.locations(), location_yaml)) as f:
                location_data = yaml.load(f.read())
            for i in range(location_data['weight']):
                variants.append(location_yaml[:-len('.yaml')])

        return random.choice(variants)

    def get(self, x, y):
        row = self.matrix.setdefault(x, {})
        if y in row:
            return row[y]
        location = Location.load(self.random_location())
        location.x = x
        location.y = y
        row[y] = location
        return location
