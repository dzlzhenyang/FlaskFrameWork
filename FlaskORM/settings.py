import os

# 配置参数
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIR = os.path.join(BASE_DIR, "static")


# 开发时使用
class Config():
    DEBUG = True
    # 使用sqlite数据库
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "ORM.sqlite")
    # 使用mysql数据库
    # SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost/db_orm"
    # 请求结束后自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # flask1版本之后添加的，目的是跟踪数据的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '123'


# 上线后
class RunConfig(Config):
    DEBUG = False
