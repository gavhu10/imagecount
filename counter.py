import flask as f


counter = f.Blueprint("api", __name__, url_prefix="/api/v1")
