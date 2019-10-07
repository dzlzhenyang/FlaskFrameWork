import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

# 实例化app
app = Flask(__name__)

# 配置参数
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# sqlite 的数据库地址
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "ORM.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/demo"
# 请求结束自动提交
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# 跟踪修改
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# orm关联应用
models = SQLAlchemy(app)


# 定义表
class Curriculum(models.Model):
    __tablename__ = "curriculum"

    id = models.Column(models.Integer, primary_key=True)
    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date)


# 创建表（同步）
# models.create_all()

# 创建操作数据库的对象
session = models.session()
# import datetime
# 增加一条
# data = Curriculum(c_id="001",c_name="python",c_time=datetime.datetime.now())
# session.add(data)
# session.commit()
# 增加多条
# data1 = Curriculum(c_id="002", c_name="java", c_time=datetime.datetime.now())
# data2 = Curriculum(c_id="003", c_name="mysql", c_time=datetime.datetime.now())
# data3 = Curriculum(c_id="004", c_name="linux", c_time=datetime.datetime.now())
# session.add_all([data1, data2, data3])
# session.commit()


# 查询所有 返回多条列表对象
# data = Curriculum.query.all()
# print(data)
# for i in data:
#     print(i.c_id, i.c_name)

# 条件查询 返回多条列表对象
# data = Curriculum.query.filter_by(c_id="001")
# for i in data:
#     print(i.c_id, i.c_name)
# data = Curriculum.query.filter(Curriculum.c_id == "001")
# for i in data:
#     print(i.c_id, i.c_name)

# 查询单条 只能通过id获取数据  返回一条列表对象
# data = Curriculum.query.get(2)
# print(data.c_id, data.c_name)

# 排序 正序
# data = Curriculum.query.order_by("id")
# for i in data:
#     print(i.c_id, i.c_name)
# 倒序
# data = Curriculum.query.order_by(models.desc("id"))
# for i in data:
#     print(i.c_id, i.c_name)

# 分页查询 从索引3开始查，查询四条数据
# 相对于sql语句的select * from curriculum limit 3,4;
# data = Curriculum.query.offset(3).limit(4)
# for i in data:
#     print(i.c_id, i.c_name)


# 删除
# 删除和修改都需要先获取数据
# data = Curriculum.query.get(1)
# session.delete(data)
# session.commit()


# 修改
# data = Curriculum.query.get(3)
# data.c_name = "JAVA"
# session.add(data)
# session.commit()
