import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

    if os.environ.get('FLASK_ENV') == 'development':
        SQLALCHEMY_DATABASE_URI = os.environ.get('EXTERNAL_DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('INTERNAL_DATABASE_URL')

    SQLALCHEMY_TRACK_MODIFICATIONS = False