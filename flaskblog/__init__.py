from flask import Flask
# from flask_uuid import FlaskUUID
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'dc859224947d25ab9cd71c15d9628b7f'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
sess_uuid = str(uuid4())
# FlaskUUID(app)

from flaskblog import routes