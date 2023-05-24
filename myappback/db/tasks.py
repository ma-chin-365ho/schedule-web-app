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
            'todo_id' : {'N': self.todo_id},
            'id': {'N': self.id},
            'title': {'S': self.title},
            'schedual_st_date': {'N': self.title},
            'schedual_st_time': {'N': self.title},
            'schedual_ed_date': {'N': self.title},
            'schedual_ed_time': {'N': self.title},
            'contents': {'S': self.title},
            'tags': {'L' : self.tags}   # tags = [{'S': "xxx"}, {'S': "yyy"}, ... ]
        }
        return json

    