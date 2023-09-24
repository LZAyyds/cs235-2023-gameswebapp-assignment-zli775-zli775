from functools import wraps

from flask import Blueprint, render_template, url_for, flash, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

from .services import validate_password
from games.domainmodel.model import User

login_bp = Blueprint('login', __name__)


@login_bp.route("/register", methods=['GET', 'POST'])
def register():
    print("Inside register function")
    from games.adapters.repository import repo_instance
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        repo_instance.add_user(new_user)
        flash('Your account has been created!', 'success')
        return redirect(url_for('login.login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@login_bp.route("/login", methods=['GET', 'POST'])
def login():
    from games.adapters.repository import repo_instance
    form = LoginForm()
    if form.validate_on_submit():
        user = repo_instance.get_user(form.username.data)
        if user and user.password == form.password.data:
            session['logged_in'] = True
            session['username'] = user.username
            flash('You have been logged in!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@login_bp.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('home.home'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('You need to login first!', 'danger')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)

    return decorated_function


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), validate_password])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
