import os
from db.dynamodb import DynamoDB

TODOS_TABLE = os.environ['TODOS_TABLE']

class Todos(DynamoDB):
    def __init__(self):
        super().__init__(TODOS_TABLE)
        self.archive_id = None
        self.id = None
        self.title = None
        self.tags = None
    
    def key_json(self, key_val):
        json = {
            'id': {'N': None}
        }
        if any(key_val):
            for k, v in key_val.items():
                # 'N'項目でもstr型にしないとboto3で型エラーになる。
                json[k] = {list(json[k].keys())[0] : str(v)}
        return json

    def item_json(self):
        json = {
            'archive_id' : {'N': self.archive_id},
            'id': {'N': self.id},
            'title': {'S': self.title},
            'tags': {'L' : self.tags}   # tags = [{'S': "xxx"}, {'S': "yyy"}, ... ]
        }
        return json

    