import os
from db.dynamodb import DynamoDB

TASKS_TABLE = os.environ['TASKS_TABLE']

class Tasks(DynamoDB):
    def __init__(self):
        super().__init__(TASKS_TABLE)
        self.todo_id = None
        self.id = None
        self.title = None
        self.schedual_st_date = None
        self.schedual_st_time = None
        self.schedual_ed_date = None
        self.schedual_ed_time = None
        self.contents = None
        self.tags = None

    def json(self):
        json = {
            'todoId' : self.todo_id,
            'id': self.id,
            'title': self.title,
            'schedualStDate': self.schedual_st_date,
            'schedualStTime': self.schedual_st_time,
            'schedualEdDate': self.schedual_ed_date,
            'schedualEdTime': self.schedual_ed_time,
            'contents': self.contents,
            'tags': self.tags
        }
        return json

    def key_json(self, key_val):
        json = {
            'todoId': {'N': None},
            'id': {'N': None}
        }
        if any(key_val):
            for k, v in key_val.items():
                # 'N'項目でもstr型にしないとboto3で型エラーになる。
                json[k] = {list(json[k].keys())[0] : str(v)}
        return json

    