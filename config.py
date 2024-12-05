import os
from urllib.parse import quote_plus

basedir = os.path.abspath(os.path.dirname(__file__))

user = "card_container_base_user"
password = quote_plus("q6z7i42DbOJRLxaUdhnonToqpd0UAL1v")
host = "dpg-ct7d5a52ng1s73cdebm0-a.frankfurt-postgres.render.com"
database = "card_container_base"
port = "5432"

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
