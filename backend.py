import datetime
import secrets

import anybadge
import io
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from flask import Request

import db


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

    increment(id, str(request.user_agent) + str(request.remote_addr))

    return image_count(id)


def increment(id: str, userdata: str) -> None:
    """Update the value of an image"""

    with db.DBConnection() as conn:
        conn.execute("UPDATE badges SET count = count + 1 WHERE id = (?)", (id,))
        conn.execute(
            "INSERT into requests (badge_id, useragent) VALUES (?, ?)", (id, userdata)
        )
        conn.commit()


def valid_color(color: str) -> bool:
    """Checks if the color is valid"""

    if color.upper() in anybadge.Color.__members__.keys():
        return True

    if color.startswith("#"):
        return True

    return False


def style(style: str) -> dict[str, str | int]:

    if style == "gitlab-scoped":
        return {"style": style, "num_padding_chars": 1}

    return {"style": "default"}


def get_data(id: str) -> list[datetime.datetime]:
    """Gets the data for processing"""

    with db.DBConnection() as conn:
        ret = conn.execute(
            "SELECT time_gotten FROM requests WHERE badge_id = (?)", (id,)
        ).fetchall()

    if not ret:
        raise ImageError("No such image!")

    return [i[0] for i in ret]


def get_graph(id: str) -> io.BytesIO:
    """Return a buffer with a png image"""

    dates = get_data(id)

    plt.switch_backend("Agg")

    fig, ax = plt.subplots()
    plt.hist(dates, bins=50)  # type: ignore
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    fig.autofmt_xdate()

    plt.title("Events Over Time")
    plt.xlabel("Time (HH:MM:SS)")
    plt.ylabel("Event Count")
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")

    return buf
