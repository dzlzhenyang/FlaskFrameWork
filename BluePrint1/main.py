from flask import Flask
from blue_print01 import simple1
from blue_print02 import simple2

app = Flask(__name__)
app.register_blueprint(simple1)
app.register_blueprint(simple2)
app.run()
