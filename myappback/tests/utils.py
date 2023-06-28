
import glob
import os
import json
import boto3
import requests
from db.dynamodb import offline_dynamodb_client, remove_type_dynamodb_json
from constants import API_URL

dynamodb_test_data = []
json_test_data = []

def load_test_json():
    global dynamodb_test_data
    global json_test_data

    tdata_paths=glob.glob('./tests/data/*')
    for td_p in tdata_paths:
        table_name = os.path.splitext(os.path.basename(td_p))[0]
        with open(td_p) as td_f:
            table_data_dicts = json.load(td_f)
        dynamodb_test_data.append((table_name, table_data_dicts))

        json_data_dicts = []
        for table_data_dict in table_data_dicts:
            json_data_dicts.append(remove_type_dynamodb_json(table_data_dict))
        json_test_data.append((table_name, json_data_dicts))
    
def import_test_data_to_dynamodb(test_tables):
    dynamodb_client = offline_dynamodb_client()
    for table_name, table_recs in test_tables:
        for table_rec in table_recs:
            dynamodb_client.put_item(
                TableName=table_name,
                Item=table_rec
            )

def get_test_json_by_tablename(table_name):
    data = []
    for tn, js in json_test_data:
        if tn == table_name:
            data = js
    return data

def ok_communication_web_server():
    r = requests.get(API_URL)
    if r.status_code == 403:
        return False
    else:
        return True