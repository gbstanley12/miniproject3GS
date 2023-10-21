# Gavin Stanley
# INF601 - Advanced Programming in Python
# miniproject3

# Importing necessary modules and libraries
import os
from flask import Flask
from . import db, auth, blog  # Importing local modules: db, auth, and blog

def create_app():
    # Creating a new Flask web application instance
    app = Flask(__name__)

    # Configuring the app with some settings
    app.config.from_mapping(
        SECRET_KEY='dev',  # Secret key for session management (using 'dev' for development purposes)
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')  # Path to the SQLite database file
    )

    # Initializing the database with the app
    db.init_app(app)

    # Registering blueprints (modular components) for authentication and blogging functionalities
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # Setting the default route to point to the 'index' endpoint
    app.add_url_rule('/', endpoint='index')

    # Returning the configured app instance
    return app
