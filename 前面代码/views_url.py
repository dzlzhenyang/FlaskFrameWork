from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"


@app.route("/list/")
def list():
    return "hello world"


@app.route("/content/<name>/<int:age>/")
def content(name, age):
    return "hello I am %s,I am %s years old" % (name, age)


import datetime


@app.route("/where_day/<int:year>/<int:month>/<int:day>/")
def where_day(year, month, day):
    now = datetime.datetime(year, 1, 1, 0, 0, 0)
    birthday = datetime.datetime(year, month, day, 0, 0, 0)
    where_day = (birthday - now).days
    return str(where_day)


@app.route("/method/", methods=["GET", "POST"])
def method():
    return "Hello, this ,is method"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
