from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from http import client as httpclient
from app import db, api
from app.models import User as UserModel
from app.schemas import UserSchema
from app.exceptions import NotFound


class User(Resource):
    def __init__(self):
        self.user_schema = UserSchema()

    @jwt_required
    def get(self, id=None):
        if id:
            user = UserModel.query.get(id)
            if user is None:
                raise NotFound()
            return self.user_schema.dump(user), httpclient.OK
        users = UserModel.query.all()

        return self.user_schema.dump(users, many=True), httpclient.OK

    def post(self):
        json_data = request.get_json()
        new_user = self.user_schema.load(json_data)

        db.session.add(new_user)
        db.session.commit()

        return self.user_schema.dump(new_user), httpclient.CREATED
        
    @jwt_required
    def put(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if user is None:
            raise NotFound()

        json_data = request.get_json()
        updated_user = self.user_schema.load(json_data)

        # manual updates to user object
        user.email = updated_user.email
        user.username = updated_user.username
        user.password_hash = updated_user.password_hash

        db.session.commit()

        return self.user_schema.dump(user)
                
    def delete(self, id):
        return NotImplementedError


class Bill(Resource):
    @jwt_required
    def get(self):
        return NotImplementedError

    @jwt_required
    def post(self):
        return NotImplementedError

    @jwt_required
    def put(self):
        return NotImplementedError

    @jwt_required
    def delete(self):
        return NotImplementedError


api.add_resource(User, '/api/users', '/api/users/<int:id>')
