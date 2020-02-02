from flask import jsonify


class ApiException(Exception):
    """ Base exception class for handling Splitter API exception """
    error_status_code = 500
    message = 'Unknown error occured'

    def __init__(self, message=None, errors=None):
        if message is not None:
            self.message = message
        self.errors = errors

    def to_dict(self):
        response = {}
        response['message'] = self.message
        if self.errors:
            response['errors'] = self.errors
        
        return response


class NotFound(ApiException):
    error_status_code = 404
    message = 'Resource not found'


class AuthenticationFailed(ApiException):
    error_status_code = 401
    message = 'Bad email or password. Please check the credentials again.'


class ParseError(ApiException):
    error_status_code = 400
    message = ''


class ValidationFailed(ApiException):
    error_status_code = 422
    message = 'Validation Failed'