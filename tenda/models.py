import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from datetime import datetime
# importing db from tenda
from tenda import db, login_manager, app
from flask_login import UserMixin

# loading user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# creating User class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))
    # relationship between user and todo_post
    todos = db.relationship('Todo', backref='author', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    # string __repr__ method
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
    
    # resetting password
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode( {'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'],\
            algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],\
                algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)

# creating Todo class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)
    # user_id acting as a foreign_key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    
    def __repr__(self):
        return f"Todo('{self.id}', '{self.title}')"
  