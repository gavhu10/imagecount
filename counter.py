from typing import Any

import anybadge
import flask as f

import backend as bk

counter = f.Blueprint("counter", __name__, url_prefix="/")


@counter.route("", methods=["GET", "POST"])
def create():
    if f.request.method == "GET":
        return f.render_template("create.html", link=f.current_app.config.get("LINK"))

    id = bk.create()

    return f.redirect(f.url_for("counter.img", id=id))


@counter.route("img")
def img():

    if f.request.args.get("id") is None:
        f.abort(404)

    color = f.request.args.get("color", "")

    if not bk.valid_color(color):
        color = "teal"

    if f.request.args.get("prev") == "true":
        try:
            times = bk.image_count(f.request.args["id"])
        except bk.ImageError as e:
            return e.message, 403
    else:
        try:
            times = bk.get_and_update(f.request.args["id"], f.request)
        except bk.ImageError as e:
            return e.message, 403

    style_args: dict[str, Any] = bk.style(f.request.args.get("style", ""), times)
    badge = anybadge.Badge(default_color=color, **style_args)

    resp = f.make_response(str(badge))
    resp.headers["Content-Type"] = "image/svg+xml"
    resp.headers["Cache-Control"] = "no-cache"

    return resp


@counter.route("graph")
def graph():

    try:
        id = f.request.args["id"]
    except IndexError:
        f.abort(404)

    try:
        data = bk.get_graph(id).getvalue()
    except bk.ImageError as e:
        return e.message, 400

    resp = f.make_response(f.Response(data, mimetype="image/png"))
    resp.headers["Cache-Control"] = "no-cache"

    return resp
