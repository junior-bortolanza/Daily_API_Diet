from database import db
from flask_login import UserMix

class User(db.Model, UserMix):
    #id, username and password, role
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

