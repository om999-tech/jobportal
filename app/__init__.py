from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.extensions import db, migrate
from flask_admin import Admin
from flask_login import LoginManager
from app.models import User
from app.models import *
# from app import admin_view
from flask_admin.contrib.sqla import ModelView
from app.auth.views import auth_bp
from app.admin_user.views import adminuser_bp
from app.employer.views import employer_bp
from app.jobseeker.views import jobseeker_bp




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    # Initialize extensions
    db.init_app(app)
    # bcrypt.init_app(app)
    migrate.init_app(app, db)
    
      # Import and initialize admin
    from app.admin_view import init_admin
    init_admin(app)

    # admin.init_app(app)
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Job, db.session))
    # admin.add_view(ModelView(Application, db.session))

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints

    app.register_blueprint(auth_bp)
    app.register_blueprint(adminuser_bp)
    app.register_blueprint(employer_bp)
    app.register_blueprint(jobseeker_bp)

    return app