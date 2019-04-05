from flask_restful import Resource


class User(Resource):
    def get(self, id=None):
        return NotImplementedError

    def post(self):
        return NotImplementedError

    def put(self, id):
        return NotImplementedError

    def delete(self, id):
        return NotImplementedError