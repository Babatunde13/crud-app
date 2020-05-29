from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import hashlib

from app import db, login_manager

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)# primary_key=True)
    username=db.Column(db.String(60), index=True, unique=True)
    first_name=db.Column(db.String(60), index=True)
    last_name=db.Column(db.String(60), index=True)
    password_hash=db.Column(db.String(128))
    department_id=db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id=db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin=db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash_ = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                                                                url=url, 
                                                                hash=hash_, 
                                                                size=size, 
                                                                default=default, 
                                                                rating=rating)

    def __repr__(self):
        return f'<Employee: {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60), unique=True)
    description=db.Column(db.String(200))
    employees=db.relation
    employees=db.relationship('Employee', 
                                backref='department', 
                                lazy='dynamic')

    def __repr__(self):
        return f'<Department: {self.name}>'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60), index=True)
    description=db.Column(db.String(200))
    employees=db.relationship('Employee',
                                backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return f'<Role: {self.name}>'
