from flask import jsonify


class ApiException(Exception):
    """ Base exception class for handling Splitter API exception """
    error_stattus_code = 500
    message = ''

    def __init__(self, message=None):
        error_stattus_code = 500
        if message is not None:
            self.message = message

    def to_dict(self):
        return {
            'error_status_code': self.error_stattus_code,
            'message': self.message
        }


class NotFound(ApiException):
    error_status_code = 404
    message = 'User not found'


class AuthenticationFailed(ApiException):
    error_stattus_code = 401
    message = 'Bad email or password. Please check the credentials again.'
