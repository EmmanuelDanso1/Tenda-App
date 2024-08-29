# using flask wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
# using validators to validate the input fields
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from tenda.models import User

# Sign Up Form
class Sign_UpForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    # validation check no email repetition
    def validate_email(self, email):
        # checking if email is already in the database
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exist. Please choose a different email')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    