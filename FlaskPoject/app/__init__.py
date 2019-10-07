from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect



# 数据库兼容
import pymysql

pymysql.install_as_MySQLdb()

# 实例化插件
models = SQLAlchemy()
api = Api()
csrf = CSRFProtect()


def create():
    # 创建app
    app = Flask(__name__)
    # 加载配置
    app.config.from_object("settings.Config")
    # 加载数据库
    models.init_app(app)
    # 加载restful
    api.init_app(app)
    # 加载csrf
    api.init_app(app)
    # 导入main中定义的蓝图
    from .main import main as main_blueprint
    # 注册蓝图
    app.register_blueprint(main_blueprint)

    return app

