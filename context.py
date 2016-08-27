class Context(object):
    def __init__(self, chat):
        self.chat = chat
        self.reset()

    def reset(self):
        self.language = None


