"""
flask当中，可以直接创建应用，进行开发，而django是先有项目，再创建应用，但是在工作当中flask
也会遇到多应用问题，也需要有项目框架，只不过这个框架被称为 蓝图（blueprint）
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"


if __name__ == "__main__":
    # app.run()
    # flask默认端口是5000
    app.run(host="127.0.0.1", port=5000, debug=True)
