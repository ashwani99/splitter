from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from http import client as httpclient
from app import db, api
from app.models import User as UserModel
from app.schemas import user_schema, user_schema_many
from app.exceptions import ResourceNotFound, ResourceAlreadyExists


class UserCollection(Resource):
    @jwt_required
    def get(self):
        users = UserModel.query.all()
        return user_schema_many.dump(users, many=True), httpclient.OK

    def post(self):
        json_data = request.get_json()
        new_user = user_schema.load(json_data)

        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ResourceAlreadyExists()

        return user_schema.dump(new_user), httpclient.CREATED

class UserResource(Resource):
    @jwt_required
    def get(self, id=None):
        if id:
            user = UserModel.query.get(id)
            if user is None:
                raise ResourceNotFound()
            return user_schema.dump(user), httpclient.OK

    @jwt_required
    def put(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if user is None:
            raise ResourceNotFound()

        json_data = request.get_json()
        updated_user = user_schema.load(json_data)

        # manual updates to user object
        user.email = updated_user.email
        user.username = updated_user.username
        user.password_hash = updated_user.password_hash

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ResourceAlreadyExists()

        return user_schema.dump(user), httpclient.OK

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


api.add_resource(UserCollection, '/api/users')
api.add_resource(UserResource, '/api/users/<int:id>')
