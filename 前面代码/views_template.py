from flask import Flask, render_template
from get_time_class import Calendar

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", **locals())


@app.route("/user_info/")
def user_info():
    calendar = Calendar().return_calendar()
    return render_template("user_info.html", **locals())


if __name__ == "__main__":
    # app.run()
    # flask默认端口是5000
    app.run(host="127.0.0.1", port=5000, debug=True)
