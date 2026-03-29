import sqlite3
from datetime import datetime
from os.path import isfile

import click
import flask as f


class DBConnection:
    """
    Class-based context manager for a sqlite3.Connection to the database defined
    in the Flask config
    Usage:
        with DBConnection() as db:
            db.execute(...)
    """

    def __init__(self):
        self.conn: sqlite3.Connection
        self._created_here: bool = False

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(
            f.current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, *_) -> bool:
        try:
            self.conn.close()
        except Exception:
            pass
        return False


def __close_db(e=None) -> None:
    """If this request connected to the database, close the connection."""
    db = f.g.pop("db", None)

    if db is not None:
        db.close()


def init_db(reset: bool) -> None:
    """Clear existing data and create new tables."""

    if reset or not isfile(f.current_app.config["DATABASE"]):
        click.echo("Creating database... ", nl=False)
        with DBConnection() as conn:
            with f.current_app.open_resource("schema.sql") as file:
                conn.executescript(file.read().decode("utf8"))
        click.echo("Done.")
    else:
        click.echo(
            "Database exists; skipping initialization. "
            "Use -r or --reset to wipe database."
        )


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)  # TODO set time zone


def init_app(app: f.Flask) -> None:
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(__close_db)
