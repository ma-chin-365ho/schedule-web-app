from flask import jsonify, request

from db.tasks import Tasks

class RestTasks():
    @staticmethod
    def get_all():
        tasks = Tasks()
        task_json = tasks.gets()
        if not task_json:
            return jsonify({'error': 'Could not find task'}), 404
        return jsonify(task_json)

    @staticmethod
    def get(todo_id):
        tasks = Tasks()
        task_json = tasks.gets(id = todo_id)
        if not task_json:
            return jsonify({'error': 'Could not find task with provided "todo_id"'}), 404
        return jsonify(task_json)

    @staticmethod
    def post():
        todo_id = request.json.get('todo_id')
        task_id = request.json.get('task_id')
        title = request.json.get('title')
        schedual_st_date = request.json.get('schedual_st_date')
        schedual_st_time = request.json.get('schedual_st_time')
        schedual_ed_date = request.json.get('schedual_ed_date')
        schedual_ed_time = request.json.get('schedual_ed_time')
        contents = request.json.get('contents')
        tags = request.json.get('tags')
        if (not todo_id or
            not task_id or
            not title or 
            not schedual_st_date or
            not schedual_st_time or
            not schedual_ed_date or
            not schedual_ed_time or
            not contents or
            not tags
        ):
            return jsonify({'error': 'Please provide both "todo_id" and "id" and "title" and ...'}), 400

        tasks = Tasks()
        tasks.todo_id = todo_id
        tasks.id = task_id
        tasks.title = title
        tasks.schedual_st_date = schedual_st_date
        tasks.schedual_st_time = schedual_st_time
        tasks.schedual_ed_date = schedual_ed_date
        tasks.schedual_ed_time = schedual_ed_time
        tasks.contents = contents
        tasks.tags = tags
        tasks.add()
        return jsonify(
            {
                'todo_id': todo_id,
                'id': task_id,
                'schedual_st_date': schedual_st_date,
                'schedual_st_time': schedual_st_time,
                'schedual_ed_date': schedual_ed_date,
                'schedual_ed_time': schedual_ed_time,
                'contents': contents,
                'tags': tags
            }
        )


    @staticmethod
    def put():
        todo_id = request.json.get('todo_id')
        task_id = request.json.get('task_id')
        title = request.json.get('title')
        schedual_st_date = request.json.get('schedual_st_date')
        schedual_st_time = request.json.get('schedual_st_time')
        schedual_ed_date = request.json.get('schedual_ed_date')
        schedual_ed_time = request.json.get('schedual_ed_time')
        contents = request.json.get('contents')
        tags = request.json.get('tags')
        if (not todo_id or
            not task_id or
            not title or 
            not schedual_st_date or
            not schedual_st_time or
            not schedual_ed_date or
            not schedual_ed_time or
            not contents or
            not tags
        ):
            return jsonify({'error': 'Please provide both "todo_id" and "id" and "title" and ...'}), 400

        tasks = Tasks()
        tasks.todo_id = todo_id
        tasks.id = task_id
        tasks.title = title
        tasks.schedual_st_date = schedual_st_date
        tasks.schedual_st_time = schedual_st_time
        tasks.schedual_ed_date = schedual_ed_date
        tasks.schedual_ed_time = schedual_ed_time
        tasks.contents = contents
        tasks.tags = tags
        tasks.update()
        return jsonify(
            {
                'todo_id': todo_id,
                'id': task_id,
                'schedual_st_date': schedual_st_date,
                'schedual_st_time': schedual_st_time,
                'schedual_ed_date': schedual_ed_date,
                'schedual_ed_time': schedual_ed_time,
                'contents': contents,
                'tags': tags
            }
        )

    @staticmethod
    def delete(task_id):
        tasks = Tasks()
        tasks.delete(id = task_id)
        return jsonify({'id': task_id})
