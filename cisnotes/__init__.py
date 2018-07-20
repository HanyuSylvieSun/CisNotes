from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '0123456789abcde0123456789abcde'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///side.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #login is the function name of the route
login_manager.login_message_category = 'info'

from cisnotes import routes
