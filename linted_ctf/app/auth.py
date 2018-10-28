from flask import Blueprint, render_template, flash, redirect, url_for, session, request, logging
from datetime import date
from wtforms import Form, StringField, TextAreaField,IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import json
from werkzeug.exceptions import abort
from app.extensions import mysql

bp = Blueprint('auth', __name__, url_prefix='/')

# User Register
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        score = str(0)
        flags = {}

        #Check to see if username is taken 
        cur = mysql.connection.cursor()
        liamNeeson = cur.execute("SELECT * from users where username = %s", [username])
        cur.close()
        if liamNeeson is not 0:
            flash('Username taken, try again.', 'danger')
            return render_template('register.html', form=form)
        
        #Check if email is taken, could probably do this more efficiently but...
        #This is the very last block of code Im adding to this project
        cur = mysql.connection.cursor()
        liamNeeson = cur.execute("SELECT * from users where email = %s", [email])
        cur.close()
        if liamNeeson is not 0:
            flash('Email already in use.', 'danger')
            return render_template('register.html', form=form)
        

        # Create cursor
        cur = mysql.connection.cursor()

        challenges = cur.execute("SELECT * FROM challenges")
        challenges = cur.fetchall()
        for chal in challenges:
            key = 'c' + str(chal['ch_id'])
            flags[key] = 0
        flags = json.dumps(flags)
        
        cur.close()

        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password, score, flags, is_admin) VALUES(%s, %s, %s, %s, %s, %s,0)", (name, email, username, password, score, flags))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


# User login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['admin'] = bool(data['is_admin'])

                flash('You are now logged in', 'success')
                return redirect(url_for('cruds.dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


@bp.errorhandler(403)
def access_denied(e):
    flash('Unauthorized action, activity logged', 'danger')
    return redirect(url_for('cruds.dashboard')), 302

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('auth.login'))
    return wrap

# Check if user is admin
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['admin'] == True:
            return f(*args, **kwargs)
        else:
            abort(403, 'Unauthorized activity')
    return wrap

# Logout
@bp.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('auth.login'))


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [
        validators.Length(min=6, max=50),
        validators.Email(message='Incorrect email format')
        ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')