import pytest
import glob
import os
import json
import boto3

from db.dynamodb import offline_dynamodb_client

def import_test_data():
    test_tables = []
    tdata_paths=glob.glob('./tests/data/*')
    for td_p in tdata_paths:
        table_name = os.path.splitext(os.path.basename(td_p))[0]
        with open(td_p) as td_f:
            table_data_dict = json.load(td_f)
        test_tables.append((table_name, table_data_dict))
    return test_tables

@pytest.fixture(scope='function')
def db_data():
    test_tables = import_test_data()

    dynamodb_client = offline_dynamodb_client()
    for table_name, table_recs in test_tables:
        print(table_name)
        for table_rec in table_recs:
            dynamodb_client.put_item(
                TableName=table_name,
                Item=table_rec
            )

    yield
    print("after test ...")
