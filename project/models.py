#Importamos el objeto de la base de datos __init__.py
from . import db
from flask_sqlalchemy import SQLAlchemy
#Importamos la clase UserMixin de  flask_login
from flask_security import UserMixin, RoleMixin

#Definiendo la tabla relacional entre usuaarios roles
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    admin=db.Column(db.Boolean,nullable=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
class Role(RoleMixin, db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
class Game(RoleMixin, db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    price = db.Column(db.String(80), unique=False)
    gender = db.Column(db.String(80), unique=False)
    platform = db.Column(db.String(100))
    image = db.Column(db.String(255),nullable=False)
