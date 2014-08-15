from app import db
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(200))
    tax_id = db.Column(db.String(16))


