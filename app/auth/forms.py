from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Regexp

from ..models import Employee

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(),
                                                Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                'Usernames must have only letters, '
                                                'numbers, dots or underscores')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[
                            DataRequired(),
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(username=field.data).first(): raise ValidationError('Email already in use')

    def validate_username(self, field):
        if Employee.query.filter_by(email=field.data).first(): raise ValidationError('Username already in use') 

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')