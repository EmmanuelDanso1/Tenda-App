from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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

# importing from route 
# import was done here to prevent circular execution
from tenda import routes