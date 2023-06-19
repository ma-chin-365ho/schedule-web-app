import pytest
import requests

from constants import API_URL
from tests.utils import get_test_json_by_tablename
from db.archives import ARCHIVES_TABLE, ARCHIVES_COUNTER_NAME
from db.dynamodb import COUNTERS_TABLE

def test_archives_get_all(db_data):
    r = requests.get(API_URL + '/archives')
    v = r.json()
    e_v = get_test_json_by_tablename(ARCHIVES_TABLE)

    assert sorted(v, key=lambda x: x['id']) == e_v
    assert r.status_code == 200

def test_archives_get(db_data):
    target_id = "3"
    r = requests.get(API_URL + '/archives/' + target_id)
    v = r.json()
    e_v = list(filter(
        lambda item : item['id'] == float(target_id),
        get_test_json_by_tablename(ARCHIVES_TABLE)
    ))[0]

    assert v == e_v
    assert r.status_code == 200

def test_archives_post(db_data):
    post_data = {
        "id" : 125,
        "title" : "テスト　22"
    }
    r = requests.post(API_URL + '/archives', json = post_data)
    assert r.status_code == 200

    target_id = str(post_data["id"])
    r = requests.get(API_URL + '/archives/' + target_id)
    v = r.json()
    e_v = dict(post_data, **{"id" : float(post_data["id"])})
    assert v == e_v
    assert r.status_code == 200

def test_archives_post_auto_increment(db_data):
    post_data = {
        "title" : "オートインクリメント　テスト　22"
    }
    id_by_counter = list(filter(
        lambda item : item['name'] == ARCHIVES_COUNTER_NAME,
        get_test_json_by_tablename(COUNTERS_TABLE)
    ))[0]['val']

    r = requests.post(API_URL + '/archives', json = post_data)
    assert r.status_code == 200

    target_id = str(int(id_by_counter+1))
    r = requests.get(API_URL + '/archives/' + target_id)
    v = r.json()
    e_v = dict(post_data, **{"id" : float(target_id)})
    assert v == e_v
    assert r.status_code == 200


def test_archives_put(db_data):
    put_data = {
        "id" : 3,
        "title" : "変更後タイトル"
    }
    r = requests.put(API_URL + '/archives', json = put_data)
    assert r.status_code == 200

    target_id = str(put_data["id"])
    r = requests.get(API_URL + '/archives/' + target_id)
    v = r.json()
    e_v = dict(put_data, **{"id" : float(put_data["id"])})
    assert v == e_v
    assert r.status_code == 200

def test_archives_delete(db_data):
    target_id = "2"
    r = requests.delete(API_URL + '/archives/' + target_id)
    assert r.status_code == 200

    r = requests.get(API_URL + '/archives/' + target_id)
    v = r.json()
    e_v = {"error": 'Could not find archive with provided "archiveId"'}
    assert v == e_v
    assert r.status_code == 404