from flask import render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            import urllib, hashlib
            
            # Set your variables here
            email = employee.email
            default = "https://www.example.com/default.jpg"
            size = 40
            
            # construct the url
            gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower().encode('utf-8')).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            login_user(employee)
            return redirect(url_for('home.dashboard', gravatar=gravatar_url))
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out")
    return redirect(url_for('auth.login'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        db.session.add(employee)
        db.session.commit()
        flash("You've registered in successfully, you can now log in")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='Register')
