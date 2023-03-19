from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
import os
#Creamos una instancia de SQLAlchemy
db = SQLAlchemy()
from .models import User, Role, Game
#Método de inicio de la aplicación
UserDataStore = SQLAlchemyUserDatastore(db,User,Role)
def create_app():
    #Creamos nuestra app en flask
    app = Flask(__name__)
    app.config['DEBUG'] = True

    #Configuraciones necesarias.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3308/flasksecurity'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha256'
    app.config['SECURITY_PASSWORD_SALT'] = 'secretsalt'

    db.init_app(app)
    #Método para crear la BD en la primera pétición
    @app.before_first_request
    def create_all():
        db.create_all()
    #Conectando los modelos de Flask-security usando SQLALCHEMY
    security = Security(app, UserDataStore)

    #Registramos dos blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app