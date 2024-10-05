''' 
Here we created model user into DB

'''

from flask_login import UserMixin
from database import db


class User(db.Model, UserMixin):
    '''id, username and password, role'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
