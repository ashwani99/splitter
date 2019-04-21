from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager

from config import Config


db = SQLAlchemy()
migrate = Migrate()
api = Api()
jwt = JWTManager()

# add resources to endpoints
from app.resources import User
api.add_resource(User, '/api/users', '/api/users/<int:id>')


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

    return app


from app import models