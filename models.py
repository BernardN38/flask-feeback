from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import session
pg_user = "tester"
pg_pwd = "testing123"

db = SQLAlchemy()
bcrypt = Bcrypt()
def connect_db(app):
    db.app = app
    db.init_app(app) 



class User(db.Model):
    __tablename__ = 'users'

    @classmethod
    def authenticate(cls,username,password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
    @classmethod
    def register(cls,username,password,email,first_name,last_name):
        password = bcrypt.generate_password_hash(password,12)
        hashed_utf8 = password.decode("utf8")
        new_user = User(username=username,password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)
        session['user_id']= new_user.username
        db.session.add(new_user)
        db.session.commit()
        return new_user

    username = db.Column(
        db.String(20),
        primary_key=True
    )
    password = db.Column(
        db.Text,
        nullable=False,
    )
    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )
    first_name = db.Column(
        db.String(30),
        nullable=False
    )
    last_name = db.Column(
        db.String(30),
        nullable=False
    )
    feedback = db.relationship('Feedback')

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False,
    )
    username = db.Column(
        db.Text,
        db.ForeignKey('users.username')
    )