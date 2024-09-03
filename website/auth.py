from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired

auth = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # Note: Replace with a proper password hash check
            login_user(user, remember=True)
            flash('Login successful!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Login failed. Check your email and/or password.', category='error')
    return render_template("login.html", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 != password2:
            flash('Passwords do not match!', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists!', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", form=form)
