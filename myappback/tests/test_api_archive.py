import pytest
import requests

from constants import API_URL

def test_archives_get_all(db_data):
    print("archive test")
    r = requests.get(API_URL + '/archives')
    print(r.json())

    assert r.status_code == 200

