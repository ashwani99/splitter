from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager

from config import Config
from app.exceptions import ApiException


db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()


def create_app(config=Config):
    """An application factory"""
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)

    # register auth blueprint
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # bind error handler
    @app.errorhandler(ApiException)
    def handle_api_exception(e):
        return make_response(jsonify(e.to_dict()), e.error_status_code)

    return app


from app import models, resources
