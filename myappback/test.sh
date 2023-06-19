#!/bin/bash
source venv/bin/activate
source setup.sh
export ARCHIVES_TABLE=archives-table-dev
export TODOS_TABLE=todos-table-dev
export TASKS_TABLE=tasks-table-dev
export COUNTERS_TABLE=counters-table-dev
export ARCHIVES_COUNTER_NAME=archives
export TODOS_COUNTER_NAME=todos
export TASKS_COUNTER_NAME=tasks

./run_dynamodb.sh &
# wait start
#sleep 5
#python -m pytest -s tests/test_api_task.py::test_tasks_put
python -m pytest -s

ps -ef | grep "serverless\sdynamodb\sstart" | grep -v grep | awk '{ print $2 }' | xargs kill
ps -ef | grep DynamoDBLocal_lib | grep -v grep | awk '{ print $2 }' | xargs kill