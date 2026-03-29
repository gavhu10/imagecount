import logging
import os

import click
import flask as f

import counter
import db


@click.command("init")
@click.option("-r", "--reset", is_flag=True)
def init_db_command(reset: bool):
    """Clear existing data and create new tables."""

    db.init_db(reset)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    logging.getLogger().setLevel(logging.INFO)
    app = f.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "db.sqlite"),
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.cli.add_command(init_db_command)

    app.register_blueprint(counter.counter)

    return app


app = create_app()
