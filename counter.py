import flask as f

import backend as bk


counter = f.Blueprint("counter", __name__, url_prefix="/")


@counter.route("", methods=["GET", "POST"])
def create():
    if f.request.method == "GET":
        return f.render_template("create.html")

    id = bk.create()

    return f.redirect(f.url_for("counter.img", id=id))


@counter.route("img")
def img():
    if not f.request.args["id"]:
        f.abort(404)

    try:
        return "Times gotten: " + str(
            bk.get_and_update(f.request.args["id"], f.request)
        )
    except bk.ImageError as e:
        return e.message, 403
