from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import Config

db = SQLAlchemy()
api = Api()


from resources import User
api.add_resource(User, '/api/users', '/api/users/<int:id>')

def create_app(config=Config):
    """An application factory"""
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    api.init_app(app)
    
    return app
