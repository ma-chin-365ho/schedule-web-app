import os
from abc import ABCMeta, abstractmethod
from decimal import Decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.types import TypeSerializer

COUNTERS_TABLE = os.environ['COUNTERS_TABLE']

dynamodb_type_deserializer = TypeDeserializer()
dynamodb_type_serializer = TypeSerializer()
dynamodb_client = boto3.client('dynamodb')

def offline_dynamodb_client():
    return boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )
if os.environ.get('IS_OFFLINE'):
    dynamodb_client = offline_dynamodb_client()

def remove_type_dynamodb_json(dynamodb_json_dict):
    json_dict = {
        k: dynamodb_type_deserializer.deserialize(v)
        for k, v in dynamodb_json_dict.items()
    }
    for k, v in json_dict.items():
         if isinstance(v, Decimal):
             json_dict[k] = float(v)
    return json_dict

def add_type_dynamodb_json(json_dict):
    dynamodb_json_dict = {
        k: dynamodb_type_serializer.serialize(v)
        for k, v in json_dict.items()
    }
    return dynamodb_json_dict

class DynamoDB(metaclass=ABCMeta):
    def __init__(self, table_name, counter_name = ""):
        self.table_name = table_name
        self.counter_name = counter_name
    
    @abstractmethod
    def json(self):
        pass

    @abstractmethod
    def key_json(self, key_val):
        pass

    def get(self, **key_val):
        if not any(key_val):
            return None

        result = dynamodb_client.get_item(
            TableName=self.table_name,
            Key=self.key_json(key_val)
        )

        item = result.get('Item')
        if not item:
            return None
        
        dict_item = remove_type_dynamodb_json(item)
        return dict_item

    def gets(self):
        # TODO:1MB制限の対応。
        result = dynamodb_client.scan(
            TableName=self.table_name
        )

        items = result.get('Items')
        if not items:
            return None

        dict_items = []
        for item in items:
            dict_items.append(remove_type_dynamodb_json(item))
        
        return dict_items

    def query(self, key_name, operator, key_value):
        args = {
            'TableName' : self.table_name,
            'KeyConditionExpression' : key_name + " " + operator + " :" + key_name + "Val",
            'ExpressionAttributeValues': {":" + key_name + "Val": dynamodb_type_serializer.serialize(key_value)}
        }

        # TODO:1MB制限の対応。
        result = dynamodb_client.query(**args)

        items = result.get('Items')
        if not items:
            return None

        dict_items = []
        for item in items:
            dict_items.append(remove_type_dynamodb_json(item))
        
        return dict_items


    def add(self):
        add_json = self.json()
        auto_inc_attr_name = "id"        
        if add_json.get(auto_inc_attr_name) is None:
            self.auto_increment(add_json, auto_inc_attr_name, self.counter_name)
            self.id = add_json[auto_inc_attr_name]
        dynamodb_client.put_item(
            TableName=self.table_name,
            Item=add_type_dynamodb_json(add_json)
        )
        # [TBD]error handling
        return
    
    def update(self):
        dynamodb_json = add_type_dynamodb_json(self.json())
        key_val = self.make_update_key_val(self.key_json(key_val = {}), dynamodb_json)
        (update_expression, expression_attribute_values) = self.make_update_expression(self.key_json(key_val = {}), dynamodb_json)

        dynamodb_client.update_item(
            TableName=self.table_name,
            Key=key_val,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        # [TBD]error handling
        return

    def make_update_key_val(self, key_json, item_json):
        key_val = {}
        items = item_json
        for k in key_json:
            key_val[k] = items[k]
        return key_val

    def make_update_expression(self, key_json, item_json):
        keys = list(key_json.keys())
        update_expression = "SET "
        expression_attribute_values = {}
        is_first = True
        for k, v in item_json.items():
            if not k in keys:
                if is_first:
                    comma = ""
                    is_first = False
                else:
                    comma = ","
                update_expression = update_expression + comma + k + "=:" + k
                expression_attribute_values[":" + k] = v

        return (update_expression, expression_attribute_values)

    def delete(self, **key_val):
        dynamodb_client.delete_item(
            TableName=self.table_name,
            Key=self.key_json(key_val)
        )
        # [TBD]error handling
        return

    def auto_increment(self, target_json, attr_name, counter_name):
        if counter_name == "":
            return
        counter_key_json = {
            'name': {'S': counter_name}
        }
        result = dynamodb_client.get_item(
            TableName=COUNTERS_TABLE,
            Key=counter_key_json
        )
        counter_item_json = result.get('Item')
        if not counter_item_json:
            return
        counter_item_json["val"]["N"] = str(int(counter_item_json["val"]["N"]) + 1)

        (update_expression, expression_attribute_values) = self.make_update_expression(counter_key_json, counter_item_json)
        dynamodb_client.update_item(
            TableName=COUNTERS_TABLE,
            Key=counter_key_json,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        target_json[attr_name] = int(counter_item_json["val"]["N"])
        return



