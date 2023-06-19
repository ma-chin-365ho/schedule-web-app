import os
from db.dynamodb import DynamoDB

ARCHIVES_TABLE = os.environ['ARCHIVES_TABLE']
ARCHIVES_COUNTER_NAME = os.environ['ARCHIVES_COUNTER_NAME']

class Archives(DynamoDB):
    def __init__(self):
        super().__init__(ARCHIVES_TABLE, ARCHIVES_COUNTER_NAME)
        self.id = None
        self.title = None
    
    def json(self):
        json = {
            'id': self.id,
            'title': self.title
        }
        return json

    def key_json(self, key_val):
        json = {
            'id': {'N': None}
        }
        if any(key_val):
            for k, v in key_val.items():
                # 'N'項目でもstr型にしないとboto3で型エラーになる。
                json[k] = {list(json[k].keys())[0] : str(v)}
        return json


    