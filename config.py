import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('INTERNAL_DATABASE_URL') or
        os.environ.get('EXTERNAL_DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
