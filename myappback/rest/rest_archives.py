from flask import jsonify, request

from db.archives import Archives

class RestArchives():
    @staticmethod
    def get_all():
        archives = Archives()
        archive_json = archives.gets()
        if not archive_json:
            return jsonify({'error': 'Could not find archive'}), 404
        return jsonify(archive_json)

    @staticmethod
    def get(archive_id):
        archives = Archives()
        archive_json = archives.get(id = archive_id)
        if not archive_json:
            return jsonify({'error': 'Could not find archive with provided "archive_id"'}), 404
        return jsonify(archive_json)

    @staticmethod
    def post():
        archive_id = request.json.get('id')
        title = request.json.get('title')
        if not archive_id or not title:
            return jsonify({'error': 'Please provide both "id" and "title"'}), 400

        archives = Archives()
        archives.id = archive_id
        archives.title = title
        archives.add()
        return jsonify({'id': archive_id, 'title': title})

    @staticmethod
    def put():
        archive_id = request.json.get('id')
        title = request.json.get('title')
        if not archive_id or not title:
            return jsonify({'error': 'Please provide both "id" and "title"'}), 400

        archives = Archives()
        archives.id = archive_id
        archives.title = title
        archives.update()
        return jsonify({'id': archive_id, 'title': title})

    @staticmethod
    def delete(archive_id):
        archives = Archives()
        archives.delete(id = archive_id)
        return jsonify({'id': archive_id})
