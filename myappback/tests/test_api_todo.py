import pytest
import requests

from constants import API_URL
from tests.utils import get_test_json_by_tablename
from db.todos import TODOS_TABLE

def test_todos_get_all(db_data):
    r = requests.get(API_URL + '/todos')
    v = r.json()
    e_v = get_test_json_by_tablename(TODOS_TABLE)

    assert sorted(v, key=lambda x: x['id']) == e_v
    assert r.status_code == 200

def test_todos_get(db_data):
    target_id = "1"
    r = requests.get(API_URL + '/todos/' + target_id)
    v = r.json()
    e_v = list(filter(
        lambda item : item['archiveId'] == float(target_id),
        get_test_json_by_tablename(TODOS_TABLE)
    ))

    assert sorted(v, key=lambda x: x['id']) == e_v
    assert r.status_code == 200

def test_todos_post(db_data):
    post_data = {
        "archiveId" : 2222,
        "id" : 45,
        "title" : "テスト　ポスト 22",
        "tags" : ["test", "test2"]
    }
    r = requests.post(API_URL + '/todos', json = post_data)
    assert r.status_code == 200

    target_id = str(post_data["archiveId"])
    r = requests.get(API_URL + '/todos/' + target_id)
    v = r.json()
    e_v = [post_data]
    assert v == e_v
    assert r.status_code == 200

def test_todos_put(db_data):
    put_data = {
        "archiveId" : 2,
        "id" : 3,
        "title" : "テスト 変更後　22",
        "tags" : ["test", "test2"]
    }
    r = requests.put(API_URL + '/todos', json = put_data)
    assert r.status_code == 200

    target_id = str(put_data["archiveId"])
    r = requests.get(API_URL + '/todos/' + target_id)
    v = list(filter(
        lambda item : item['id'] == float(put_data["id"]),
        r.json()
    ))    
    e_v = [put_data]
    assert v == e_v
    assert r.status_code == 200

def test_todos_delete(db_data):
    target_archive_id = "2"
    target_id = "4"
    r = requests.delete(API_URL + '/todos/' + target_archive_id + '/' + target_id)
    assert r.status_code == 200

    r = requests.get(API_URL + '/todos/' + target_archive_id)
    v = list(filter(
        lambda item : item['id'] == float(target_id),
        r.json()
    ))
    e_v = []
    assert v == e_v
    assert r.status_code == 200