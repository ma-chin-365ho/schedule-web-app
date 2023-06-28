import pytest
import requests

from constants import API_URL
from tests.utils import get_test_json_by_tablename
from db.tasks import TASKS_TABLE, TASKS_COUNTER_NAME
from db.dynamodb import COUNTERS_TABLE

def test_tasks_get_all(db_data, web_access):
    r = requests.get(API_URL + '/tasks')
    v = r.json()
    e_v = get_test_json_by_tablename(TASKS_TABLE)

    assert sorted(v, key=lambda x: x['id']) == e_v
    assert r.status_code == 200

def test_tasks_get(db_data, web_access):
    target_id = "2"
    r = requests.get(API_URL + '/tasks/' + target_id)
    v = r.json()
    e_v = list(filter(
        lambda item : item['todoId'] == float(target_id),
        get_test_json_by_tablename(TASKS_TABLE)
    ))

    assert sorted(v, key=lambda x: x['id']) == e_v
    assert r.status_code == 200

def test_tasks_post(db_data, web_access):
    post_data = {
        "todoId" : 111111,
        "id": 1000,
        "title": "テストポスト・・・タイトル",
        "schedualStDate": 20201201,
        "schedualStTime": 0,
        "schedualEdDate": 20210101,
        "schedualEdTime": 1800,
        "contents": "テスト　　テスト",
        "tags": ["aaaaaa", "test"]
    }
    r = requests.post(API_URL + '/tasks', json = post_data)
    assert r.status_code == 200

    target_id = str(post_data["todoId"])
    r = requests.get(API_URL + '/tasks/' + target_id)
    v = r.json()
    e_v = [post_data]

    assert v == e_v
    assert r.status_code == 200

def test_tasks_post_auto_increment(db_data, web_access):
    post_data = {
        "todoId" : 121212,
        "title": "テストポスト・・・タイトル",
        "schedualStDate": 20211201,
        "schedualStTime": 0,
        "schedualEdDate": 20211220,
        "schedualEdTime": 1801,
        "contents": "インクリメント　テスト　　テスト",
        "tags": ["aaaaaa", "test"]
    }
    id_by_counter = list(filter(
        lambda item : item['name'] == TASKS_COUNTER_NAME,
        get_test_json_by_tablename(COUNTERS_TABLE)
    ))[0]['val']

    r = requests.post(API_URL + '/tasks', json = post_data)
    assert r.status_code == 200

    target_id = str(post_data["todoId"])
    r = requests.get(API_URL + '/tasks/' + target_id)
    v = r.json()
    e_v = [dict(post_data, **{"id" : id_by_counter+1})]
    assert v == e_v
    assert r.status_code == 200


def test_tasks_put(db_data, web_access):
    put_data = {
        "todoId" : 3,
        "id": 5,
        "title": "変更後テストポスト・・・タイトル",
        "schedualStDate": 20201201,
        "schedualStTime": 0,
        "schedualEdDate": 20210101,
        "schedualEdTime": 1800,
        "contents": "変更後テスト　　テスト",
        "tags": ["after", "update"]
    }
    r = requests.put(API_URL + '/tasks', json = put_data)
    assert r.status_code == 200

    target_id = str(put_data["todoId"])
    r = requests.get(API_URL + '/tasks/' + target_id)
    v = list(filter(
        lambda item : item['id'] == float(put_data["id"]),
        r.json()
    ))
    e_v = [put_data]
    assert v == e_v
    assert r.status_code == 200

def test_tasks_delete(db_data, web_access):
    target_todo_id = "2"
    target_id = "1"
    r = requests.delete(API_URL + '/tasks/' + target_todo_id + '/' + target_id)
    assert r.status_code == 200

    r = requests.get(API_URL + '/tasks/' + target_todo_id)
    v = list(filter(
        lambda item : item['id'] == float(target_id),
        r.json()
    ))
    e_v = []
    assert v == e_v
    assert r.status_code == 200