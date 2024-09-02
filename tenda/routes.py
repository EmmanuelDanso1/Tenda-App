from flask import render_template, url_for,flash, redirect
# import app from init file
from tenda import app, db, bcrypt
from tenda.forms import Sign_UpForm, LoginForm
from tenda.models import User, Todo
from flask_login import login_user, current_user, logout_user

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",  title="Home")


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
    # if user is already authenticated redirect user to todo page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # check if form is validated
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check either email or password', 'danger')
    return render_template("login.html", title='Login', form=form)

# logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))