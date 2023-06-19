import os
from db.dynamodb import DynamoDB, COUNTERS_TABLE

# COUNTERS_TABLE = os.environ['COUNTERS_TABLE']

class Counters(DynamoDB):
    def __init__(self):
        super().__init__(COUNTERS_TABLE)
        self.name = None
        self.val = None
    
    def key_json(self, key_val):
        json = {
            'name': {'S': None}
        }
        if any(key_val):
            for k, v in key_val.items():
                # 'N'項目でもstr型にしないとboto3で型エラーになる。
                json[k] = {list(json[k].keys())[0] : str(v)}
        return json

    def item_json(self):
        json = {
            'name': {'S': self.name},
            'val': {'N': self.value}
        }
        return json

    