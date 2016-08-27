class Context(object):
    def __init__(self, chat):
        self.chat = chat
        self.reset()

    def as_dict(self):
        return {
            'chat_id': self.chat.id,
            'username': self.chat.username,
            'language': self.language,
        }

    def reset(self):
        self.language = None


