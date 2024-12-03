import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://card_container_base_user:q6z7i42DbOJRLxaUdhnonToqpd0UAL1v@dpg-ct7d5a52ng1s73cdebm0-a.frankfurt-postgres.render.com/card_container_base') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False