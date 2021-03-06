from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

from http import client as httpclient
from app import jwt
from app.schemas import UserLoginSchema
from app.models import User


bp = Blueprint('auth', __name__)


login_schema = UserLoginSchema()


@bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    data, errors = login_schema.load(json_data)
    if errors:
        return jsonify(errors), httpclient.UNPROCESSABLE_ENTITY
    user = User.query.filter_by(email=data['email']).scalar()
    if user and user.verify_password(data['password']):
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token), httpclient.OK
    return jsonify(msg='Bad email or password. Please check the credentials again.'), httpclient.UNAUTHORIZED


@jwt.user_identity_loader
def get_user_id(user):
    return user.id


@jwt.user_loader_callback_loader
def load_user(id):
    return User.query.get(id)