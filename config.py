import os


default_secret_key = os.urandom(24).hex()


class Config:
    """Contains application wide configuration"""
    
    SECRET_KEY = os.environ.get('SPLITTER_SECRET', default_secret_key)
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    
    # workaround for using both on Windows and linux
    if os.name == 'nt':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                                'sqlite:///{}'.format(os.path.join(BASEDIR, 'app.db')))
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                                'sqlite:////{}'.format(os.path.join(BASEDIR, 'app.db')))
                                                
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True # for testing SQL commands
    
    JWT_SECRET_KEY = os.environ.get('SPLITTER_SECRET', default_secret_key)


class TestConfig(Config):
    """Contains test environment specific configurations"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    