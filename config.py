import yaml

class Config(object):
    def __init__(self, telegram={}, log={}, storage={}):
        self.telegram_token = telegram.get('token')
        self.log_level = log.get('level', 'WARNING')
        self.storage_file = storage.get('file', 'data.yaml')

    @classmethod
    def load(cls, data):
        parsed_data = yaml.load(data)
        return Config(**parsed_data)

    def save(self):
        return yaml.dump({
            'telegram': {
                'token': self.telegram_token,
            },
            'log': {
                'level': self.log_level,
            },
            'storage': {
                'file': self.storage_file,
            }
        })


