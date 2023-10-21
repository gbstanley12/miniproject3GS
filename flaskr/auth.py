from flask import Blueprint, flash, redirect, render_template, request, url_for, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from .db import get_db

# Creating a Blueprint named 'auth' for authentication-related routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Decorator to ensure the user is logged in before accessing certain views
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Before each request, load the logged-in user's data if available
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

    g.current_user = g.user

# Route for logging in
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # Check if the user exists and the password is correct
        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# Route for registering a new user
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # Basic validation for username and password
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # Check if the username is already taken
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        # If no errors, insert the new user into the database
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

# Route for logging out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
