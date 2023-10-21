from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db

# Creating a Blueprint named 'blog' for blog-related routes
bp = Blueprint('blog', __name__)

# Route to display all blog posts
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

# Route to create a new blog post
@bp.route('/create', methods=('GET', 'POST'))
@login_required  # Ensure the user is logged in
def create():
    title = ''
    body = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        # Basic validation for title and body
        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

# Route to edit an existing blog post
@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required  # Ensure the user is logged in
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        # Basic validation for title and body
        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# Route to delete a blog post
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required  # Ensure the user is logged in
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

# Helper function to get a specific post by its ID
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    # Check if the current user is the author of the post
    if check_author and post['author_id'] != g.user['id']:
        abort(403, "You do not have permission to edit this post.")

    return post

# Route to display the roster page
@bp.route('/roster')
def roster():
    return render_template('roster.html')

# Route to display the schedule page
@bp.route('/schedule')
def schedule():
    return render_template('schedule.html')
