from flask import render_template, url_for,flash, redirect, request, jsonify
# import app from init file
from tenda import app, db, bcrypt, mail
from tenda.forms import Sign_UpForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from tenda.email import send_password_reset_email
from tenda.models import User, Todo
from flask_login import login_user, current_user, logout_user, login_required
import sqlalchemy as sa

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",  title="Home")

# todo
@app.route("/todo", methods=["GET", "POST"])
@login_required  # Ensure the user is logged in
def todo():
    if request.method == "POST":
        todo_title = request.form['title']
        todo_desc = request.form['description']
        
        # Ensure current_user is available and has an id
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            # Handle the case where user is not authenticated
            return redirect(url_for('login'))  # or handle the error appropriately

        # Create a new Todo linked to the current user
        data = Todo(title=todo_title, description=todo_desc, user_id=user_id)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('todo'))  # Redirect to the same route to see the updated list

    # Query all todos and pass to the template
    alltodo = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template("todo.html", title="Todo", alltodo=alltodo)

# sign up
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = Sign_UpForm()
    if form.validate_on_submit():
        # hashing password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # instance of a user
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created successfully. You can login now!", "success")
        return redirect(url_for('login'))
    return render_template("sign_up.html", title="Sign up", form=form)

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo'))

    form = LoginForm(request.form)  # Initialize the form with request.form if you're using Flask-WTF

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('todo'))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")

    return render_template("login.html", title='Login', form=form)

# logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# update
@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_todo(id):
    todo = Todo.query.get_or_404(id)    
    if request.method == "POST":
        todo_title = request.form['title']
        todo_desc = request.form['description']
        todo.title = todo_title
        todo.description = todo_desc
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo'))
    return render_template('update.html', todo=todo)


#  delete todo
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user.id:
        return "You do not have permission to delete this todo."
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo'))




# reset password
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )
        if user:
            send_password_reset_email(user)
        flash('Please check your email for the instructions to reset your password', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


# finally Resetting user password
@app.route('/reset_password/<token>', methods=['GET', 'POST']) 
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.", 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
