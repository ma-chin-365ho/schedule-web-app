from flask import jsonify, request

from db.todos import Todos

class RestTodos():
    @staticmethod
    def get_all():
        todos = Todos()
        todo_json = todos.gets()
        if not todo_json:
            return jsonify({'error': 'Could not find todo'}), 404
        return jsonify(todo_json)

    @staticmethod
    def get(archive_id):
        todos = Todos()
        todo_json = todos.gets(id = archive_id)
        if not todo_json:
            return jsonify({'error': 'Could not find todo with provided "archive_id"'}), 404
        return jsonify(todo_json)

    @staticmethod
    def post():
        archive_id = request.json.get('archive_id')
        todo_id = request.json.get('id')
        title = request.json.get('title')
        tags = request.json.get('tags')
        if (not archive_id or
            not todo_id or
            not title or 
            not tags
        ):
            return jsonify({'error': 'Please provide both "archive_id" and "id" and "title" and "tags"'}), 400

        todos = Todos()
        todos.archive_id = archive_id
        todos.id = todo_id
        todos.title = title
        todos.tags = tags
        todos.add()
        return jsonify({'archive_id': archive_id, 'id': todo_id, 'title': title, 'tags': tags})

    @staticmethod
    def put():
        archive_id = request.json.get('archive_id')
        todo_id = request.json.get('id')
        title = request.json.get('title')
        tags = request.json.get('tags')
        if (not archive_id or
            not todo_id or
            not title or 
            not tags
        ):
            return jsonify({'error': 'Please provide both "archive_id" and "id" and "title"'}), 400

        todos = Todos()
        todos.archive_id = archive_id
        todos.id = todo_id
        todos.title = title
        todos.tags = tags
        todos.update()
        return jsonify({'archive_id': archive_id, 'id': todo_id, 'title': title, 'tags': tags})

    @staticmethod
    def delete(todo_id):
        todos = Todos()
        todos.delete(id = todo_id)
        return jsonify({'id': todo_id})
