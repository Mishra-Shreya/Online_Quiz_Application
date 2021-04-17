from flask_login import UserMixin
from .extensions import db 

class User(UserMixin, db.Model):
    __tablename__= 'registered users'
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(1000))
    dob = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))