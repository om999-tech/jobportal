from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin

db = SQLAlchemy()
migrate = Migrate()
# bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin()

