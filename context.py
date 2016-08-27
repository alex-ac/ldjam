class Context(object):
    def __init__(self, chat):
        self.chat = chat
        self.reset()

    def as_dict(self):
        return self.__dict__

    def reset(self):
        self.language = None


