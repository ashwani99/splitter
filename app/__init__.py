from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import flask_restful
from werkzeug.exceptions import BadRequest

from config import Config
from app.exceptions import ApiException, ParseError


class SplitterAPI(flask_restful.Api):
    """ Wrapper around `flask_restful.Api` with specifics for Splitter API """

    # Flask-Restful's error handling mechanism doesn't follow Flask.errorhandler specs
    # overriding `flask_restful.Api.handle_error` to serialize all internal exceptions to JSON
    def handle_error(self, e):
        if isinstance(e, ApiException):
            # for un-handled exceptions, leave them as it is for now
            # TODO: add logging, wrap the un-handled exceptions into `ApiException`
            return make_response(jsonify(e.to_dict()), e.error_status_code)
        else:
            raise


db = SQLAlchemy()
migrate = Migrate()
api = SplitterAPI()
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

    @app.before_request
    def check_json_body():
        # make API request inputs compulsory having `application/json` mimetype
        methods_require_json = ('POST', 'PUT', 'PATCH')
        if request.method in methods_require_json:
            if not request.is_json:
                raise ParseError(message='Body should be a JSON object')
            else:
                try:
                    request.get_json()
                except BadRequest as e:
                    raise ParseError(message=e.description)

    # bind error handler for `Flask` routes
    # needed for `auth` blueprint
    @app.errorhandler(ApiException)
    def handle_api_exception(e):
        return make_response(jsonify(e.to_dict()), e.error_status_code)

    return app


from app import models, resources
