from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from os import path

db = SQLAlchemy()
csrf = CSRFProtect()  # Initialize CSRFProtect
DB_NAME = "creator.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yuteruoyqeirj ohwgj'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    csrf.init_app(app)  # Enable CSRF protection
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    return app
