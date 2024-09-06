import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
app = Flask(__name__)

# setting up SECRET KEY prevent attacks and cross side effects
app.config['SECRET_KEY'] = 'd19eb471cfc73db1cfb9ed4ee8d87d8d'
# setting up the DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tenda.db'
# creating an instance of DATABASE
db = SQLAlchemy(app)
#instance  bcrypt for hashing password
bcrypt = Bcrypt(app)
# instance for LoginManger
login_manager = LoginManager(app)
load_dotenv()

# email and mailing configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['ADMINS'] = 'kwekudanso21@gmail.com'
mail = Mail(app)

# importing from route 
# import was done here to prevent circular execution
from tenda import routes
from tenda.models import User, Todo

# setting up migration
migrate = Migrate(app, db)