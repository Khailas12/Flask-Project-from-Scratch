from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = "caeed4eb8e902df314522f2d"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)   # for security of every password in db which manupulated in hash
# When a password has been “hashed” it means it has been turned into a scrambled representation of itself

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes









