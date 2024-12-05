from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # __table_args__ = {'schema': 'public'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    cards = db.relationship('Card', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Card(db.Model):
    __tablename__ = 'cards'
    # __table_args__ = {'schema': 'public'}
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(128), nullable=False)
    translation = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
