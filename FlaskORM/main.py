# 加载数据库配置
import os
from flask import Flask
from settings import Config
# from flask_wtf import CSRFProtect  # 引入csrf保护
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# 实例化app
app = Flask(__name__)

# settings中不定义类时这么使用
# app.config.from_pyfile("settings.py")
# 有类直接使用
app.config.from_object(Config)

# ORM关联应用
models = SQLAlchemy(app)

# csrf = CSRFProtect(app)  # 使用csrf
api = Api(app)
migrate = Migrate(app, models)
