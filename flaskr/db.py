import sqlite3
import click
from flask import current_app, g

# Function to get a database connection
def get_db():
    # Check if a database connection already exists in the application context
    if 'db' not in g:
        # If not, create a new connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Use the Row factory to access rows as dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db

# Function to close the database connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Function to initialize the database using the schema
def init_db():
    db = get_db()

    # Open the schema file and execute its content to set up the database tables
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Command to initialize the database, to be used with Flask's command line interface
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Function to register database functions with the Flask app
def init_app(app):
    # Register the function to be called when the application context is torn down
    app.teardown_appcontext(close_db)
    # Add the init-db command to the application's command line interface
    app.cli.add_command(init_db_command)
