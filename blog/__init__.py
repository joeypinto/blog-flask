from flask import Flask
from blog.views import views
from blog.config import db

from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from blog.auth import auth
    from blog.admin import admin
    from blog.views import views
    from blog.errors import errors
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(errors)
    app.register_blueprint(auth)
    db.create_all(app=app)
    from blog.models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    
    return app
