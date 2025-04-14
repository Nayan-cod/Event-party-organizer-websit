# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    role = SelectField('Register As', choices=[('customer', 'Customer'), ('organizer', 'Organizer')])
    name = StringField('Name', validators=[
        InputRequired(message="Name is required."), 
        Length(min=3, max=100, message="Name must be between 3 and 100 characters.")
    ])
    email = StringField('Email', validators=[
        InputRequired(message="Email is required."), 
        Email(message="Please enter a valid email address.")
    ])
    mobile = StringField('Mobile Number', validators=[
        InputRequired(message="Mobile number is required."),
        Regexp(r'^[6-9]\d{9}$', message="Enter a valid 10-digit Indian mobile number.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required."), 
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(message="Email is required."), 
        Email(message="Please enter a valid email address.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required.")
    ])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')], validators=[InputRequired()])
    comment = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Submit Review')