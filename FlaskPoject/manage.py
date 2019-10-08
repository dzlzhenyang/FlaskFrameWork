from app import create, models
from flask_script import Manager
from gevent import monkey
from flask_migrate import Migrate, MigrateCommand

app = create()
manage = Manager(app)
migrate = Migrate(app, models)
app.secret_key = "123"
manage.add_command("db", MigrateCommand)

# 猴子补丁，将当前不契合地方的代码修改为契合，提高代码的兼容性
monkey.patch_all()


# 添加一条命令
# @manage.command
# def migrate():
#     models.create_all()

# 添加 gevent运行命令
@manage.command
def runserver_gevent():
    """
    当前代码用于io频繁的flask项目，可以提高flask项目的效率
    """
    from gevent import pywsgi
    server = pywsgi.WSGIServer(("127.0.0.1", 5000), app)
    server.serve_forever()


if __name__ == '__main__':
    # flask自带的启动项目的命令 shell,runserver
    manage.run()
