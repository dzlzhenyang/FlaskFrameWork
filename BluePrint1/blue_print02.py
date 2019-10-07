from flask import Blueprint

simple2 = Blueprint("simple2_pages", __name__)


@simple2.route("/02")
def index():
    return "hello2"
