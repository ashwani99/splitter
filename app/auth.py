from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

from app import jwt
from app.schemas import UserLoginSchema
from app.models import User
from app import exceptions


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
    
    raise exceptions.AuthenticationFailed()


@jwt.user_identity_loader
def get_user_id(user):
    return user.id


@jwt.user_loader_callback_loader
def load_user(id):
    return User.query.get(id)


@jwt.unauthorized_loader
def wrap_no_token_error():
    raise exceptions.AuthenticationFailed(message='Missing Authentication header')


@jwt.expired_token_loader
def wrap_token_expired_error():
    exceptions.AuthenticationFailed(message='Token has expired')


