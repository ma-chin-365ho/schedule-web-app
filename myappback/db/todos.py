import os
from boto3.dynamodb.conditions import Key

from db.dynamodb import DynamoDB

TODOS_TABLE = os.environ['TODOS_TABLE']
TODOS_COUNTER_NAME = os.environ['TODOS_COUNTER_NAME']

class Todos(DynamoDB):
    def __init__(self):
        super().__init__(TODOS_TABLE, TODOS_COUNTER_NAME)
        self.archive_id = None
        self.id = None
        self.title = None
        self.tags = None
    
    def json(self):
        json = {
            'archiveId' : self.archive_id,
            'id': self.id,
            'title': self.title,
            'tags': self.tags
        }
        return json

    def key_json(self, key_val):
        json = {
            'archiveId': {'N': None},
            'id': {'N': None}
        }
        if any(key_val):
            for k, v in key_val.items():
                # 'N'項目でもstr型にしないとboto3で型エラーになる。
                json[k] = {list(json[k].keys())[0] : str(v)}
        return json
