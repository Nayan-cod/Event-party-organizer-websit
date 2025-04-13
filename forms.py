# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,TextAreaField
from wtforms.validators import InputRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    role = SelectField('Register As', choices=[('customer', 'Customer'), ('organizer', 'Organizer')])
    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    mobile = StringField('Mobile Number', validators=[
        InputRequired(),
        Regexp(r'^[6-9]\d{9}$', message="Enter a valid 10-digit Indian mobile number")
    ])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')], validators=[InputRequired()])
    comment = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Submit Review')