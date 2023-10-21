from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import get_db

bp = Blueprint('polls', __name__)

# Database Model for Poll
class Poll:
    def __init__(self, id=None, question=None):
        self.id = id
        self.question = question

# Database Model for Option
class Option:
    def __init__(self, id=None, option_text=None, poll_id=None, votes=0):
        self.id = id
        self.option_text = option_text
        self.poll_id = poll_id
        self.votes = votes

@bp.route('/poll/<int:poll_id>', methods=('GET', 'POST'))
def vote(poll_id):
    db = get_db()
    poll = db.execute('SELECT * FROM poll WHERE id = ?', (poll_id,)).fetchone()
    options = db.execute('SELECT * FROM option WHERE poll_id = ?', (poll_id,)).fetchall()

    if request.method == 'POST':
        selected_option_id = request.form.get('option')
        db.execute('UPDATE option SET votes = votes + 1 WHERE id = ?', (selected_option_id,))
        db.commit()
        return redirect(url_for('polls.results', poll_id=poll_id))

    return render_template('poll.html', poll=poll, options=options)

@bp.route('/results/<int:poll_id>')
def results(poll_id):
    db = get_db()
    poll = db.execute('SELECT * FROM poll WHERE id = ?', (poll_id,)).fetchone()
    options = db.execute('SELECT * FROM option WHERE poll_id = ?', (poll_id,)).fetchall()
    return render_template('results.html', poll=poll, options=options)

