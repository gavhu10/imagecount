import db
import secrets
from flask import Request


class ImageError(Exception):
    """Custom exception for image errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def create() -> str:
    """Creates a new image and returns the token for it"""

    id = secrets.token_urlsafe(16)

    with db.DBConnection() as conn:
        conn.execute("INSERT INTO badges (id, count) VALUES (?, 0)", (id,))
        conn.commit()

    return id


def image_count(id: str) -> int:
    """Gets the count for an image"""

    with db.DBConnection() as conn:
        ret = conn.execute("SELECT count FROM badges WHERE id = (?)", (id,)).fetchone()

    if ret is None:
        raise ImageError("No such image")

    return ret[0]


def get_and_update(id: str, request: Request) -> int:
    """Get and update the value for an image"""

    increment(id, str(request.user_agent))  # TODO record ip?

    return image_count(id)


def increment(id: str, useragent: str) -> None:
    """Update the value of an image"""

    with db.DBConnection() as conn:
        conn.execute("UPDATE badges SET count = count + 1 WHERE id = (?)", (id,))
        conn.execute(
            "INSERT into requests (badge_id, useragent) VALUES (?, ?)", (id, useragent)
        )
        conn.commit()
