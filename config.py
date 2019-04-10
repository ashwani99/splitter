import os


class Config:
    """Contains application wide configuration"""
    
    SECRET_KEY = os.environ.get('SPLITTER_SECRET', 'some-very-secret-key-that-nobody-knows')
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                            'sqlite:////{}'.format(os.path.join(BASEDIR, 'app.db')))