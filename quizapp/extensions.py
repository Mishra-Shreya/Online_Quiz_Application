from flask_login import LoginManager
from flask_sqlalchemy import *

login_manager = LoginManager()
db = SQLAlchemy()