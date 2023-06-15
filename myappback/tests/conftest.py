import pytest
import time

from tests.utils import load_test_json, import_test_data_to_dynamodb, dynamodb_test_data

@pytest.fixture(scope='module')
def db_data():
    global dynamodb_test_data

    load_test_json()

    for _ in range(20):
        try:
            import_test_data_to_dynamodb(dynamodb_test_data)
        except Exception as e:
            print(type(e))
            time.sleep(1)
        else:
            break

    yield
    import_test_data_to_dynamodb(dynamodb_test_data)
    #print("after test ...")
