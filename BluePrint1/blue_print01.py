from flask import Blueprint

simple1 = Blueprint("simple_page1", __name__)


@simple1.route("/01")
def index():
    return "hello1"
