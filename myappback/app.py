import os

from flask import Flask, jsonify, make_response

from rest.rest_archives import RestArchives
from rest.rest_todos import RestTodos
from rest.rest_tasks import RestTasks

app = Flask(__name__)

# =============================================
# REST API
# =============================================
@app.route('/archives')
def get_all_archive():
    return RestArchives.get_all()

@app.route('/archives/<int:archive_id>')
def get_archive(archive_id):
    return RestArchives.get(archive_id)

@app.route('/archives', methods=['POST'])
def post_archive():
    return RestArchives.post()

@app.route('/archives', methods=['PUT'])
def put_archive():
    return RestArchives.put()

@app.route('/archives/<int:archive_id>', methods=['DELETE'])
def delete_archive(archive_id):
    return RestArchives.delete(archive_id)


@app.route('/todos')
def get_all_todo():
    return RestTodos.get_all()

@app.route('/todos/<int:archive_id>')
def get_todo(archive_id):
    return RestTodos.get_by_archive_id(archive_id)

@app.route('/todos', methods=['POST'])
def post_todo():
    return RestTodos.post()

@app.route('/todos', methods=['PUT'])
def put_todo():
    return RestTodos.put()

@app.route('/todos/<int:archive_id>/<int:todo_id>', methods=['DELETE'])
def delete_todo(archive_id, todo_id):
    return RestTodos.delete(archive_id, todo_id)


@app.route('/tasks')
def get_all_task():
    return RestTasks.get_all()

@app.route('/tasks/<int:todo_id>')
def get_task(todo_id):
    return RestTasks.get_by_todo_id(todo_id)

@app.route('/tasks', methods=['POST'])
def post_task():
    return RestTasks.post()

@app.route('/tasks', methods=['PUT'])
def put_task():
    return RestTasks.put()

@app.route('/tasks/<int:todo_id>/<int:task_id>', methods=['DELETE'])
def delete_task(todo_id, task_id):
    return RestTasks.delete(todo_id, task_id)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
