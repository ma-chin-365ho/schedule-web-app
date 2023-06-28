import pytest
import time

from tests.utils import load_test_json, import_test_data_to_dynamodb, dynamodb_test_data, ok_communication_web_server
from constants import  RETRYCNT_SEC_DYNAMODB, TIMEOUT_SEC_WEB_ACCESS

@pytest.fixture(scope='module')
def db_data():
    global dynamodb_test_data

    load_test_json()

    for i in range(RETRYCNT_SEC_DYNAMODB+1):
        if i < (RETRYCNT_SEC_DYNAMODB):
            try:
                import_test_data_to_dynamodb(dynamodb_test_data)
            except Exception as e:
                print(type(e))
                time.sleep(1)
            else:
                break
        else:
            import_test_data_to_dynamodb(dynamodb_test_data)

    yield
    import_test_data_to_dynamodb(dynamodb_test_data)
    #print("after test ...")

@pytest.fixture(scope='session')
def web_access():
    for i in range(TIMEOUT_SEC_WEB_ACCESS):
        if i < (TIMEOUT_SEC_WEB_ACCESS-1):
            try:
                if not ok_communication_web_server():
                    raise ConnectionError
            except Exception as e:
                print(type(e))
                time.sleep(1)
            else:
                break
        else:
            if not ok_communication_web_server():
                raise ConnectionError