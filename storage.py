import yaml

class Storage(object):
    def __init__(self, last_update_id=None):
        self.last_update_id = None
    
    @classmethod
    def load(cls, data):
        return cls(**yaml.load(data))

    def save(self):
        return yaml.dump({
            'last_update_id': self.last_update_id,
        })


