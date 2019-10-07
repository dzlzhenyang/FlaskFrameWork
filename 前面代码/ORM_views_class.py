import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql

pymysql.install_as_MySQLdb()

# 实例化app
app = Flask(__name__)

# 配置参数
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# sqlite数据库地址
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "ORM.salite")
# mysql
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/demo"
# 请求结束后自动提交
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# 跟踪修改
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# ORM关联应用
models = SQLAlchemy(app)


class BaseModel(models.Model):
    # 声明当前类是抽象类，可以被继承调用，不可以被创建
    __abstract__ = True
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        session = models.session()
        session.add(self)
        session.commit()

    def delete(self):
        session = models.session()
        session.delete(self)
        session.commit()


class Course(BaseModel):
    __tablename__ = "course"
    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date())


# models.create_all()

# if __name__ == '__main__':
    # data = Course.query.get(3)
    # data.delete()
