from datetime import datetime
# importing db from tenda
from tenda import db, login_manager
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
    # relationship between user and todo_post
    todos = db.relationship('Todo', backref='author', lazy=True)

    # string __repr__ method
    def __repr__(self):
        return f"User({self.name}, {self.email})"

# creating Todo class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # user_id acting as a foreign_key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    
    def __repr__(self):
        return f"Todo({self.id}, {self.title})"