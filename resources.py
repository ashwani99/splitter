from flask import request, jsonify
from flask_restful import Resource
from marshmallow import post_load
from sqlalchemy.exc import IntegrityError

from http import client as httpclient
from app import db
from models import User as UserModel
from schemas import UserSchema


def error_template(message, status_code):
    return {'message': {'error': message}}, status_code


class User(Resource):
    def __init__(self):
        self.user_schema = UserSchema()

    def get(self, id=None):
        if id:
            user = UserModel.query.get(id)
            if user is None:
                return error_template('User not found', httpclient.NOT_FOUND)
            return self.user_schema.dump(user).data, httpclient.OK
        users = UserModel.query.all()
        return self.user_schema.dump(users, many=True).data, httpclient.OK

    def post(self):
        json_data = request.get_json()
        data, errors = self.user_schema.load(json_data)
        if errors:
            return errors, httpclient.UNPROCESSABLE_ENTITY

        user = UserModel(email=data['email'], username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return self.user_schema.dump(user).data, httpclient.CREATED
        
    def put(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if user is None:
            return error_template('User not found', httpclient.NOT_FOUND)
        json_data = request.get_json()
        data, errors = self.user_schema.load(json_data)
        if errors:
            return errors, httpclient.UNPROCESSABLE_ENTITY
        for attr, value in data.items():
            if attr is 'password':
                user.set_password(value)
                continue
            if getattr(user, attr) != value:
                setattr(user, attr, value)
        db.session.commit()

        return self.user_schema.dump(user).data
                
    def delete(self, id):
        return NotImplementedError