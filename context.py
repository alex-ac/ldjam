from map import Map

class Context(object):
    def __init__(self, chat):
        self.chat = chat
        self.reset()

    def as_dict(self):
        return self.__dict__

    def reset(self):
        self.language = None
        self.location = None
        self.item_in_hands = None
        self.inventory = None
        self.map = Map()
