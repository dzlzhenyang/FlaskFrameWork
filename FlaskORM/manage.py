from flask_script import Manager
from flask_migrate import MigrateCommand

from views import app
from models import models

manage = Manager(app)

# 添加一条命令
# @manage.command
# def migrate():
#     models.create_all()

manage.add_command("db", MigrateCommand)

if __name__ == '__main__':
    # flask自带的启动项目的命令 shell,runserver
    manage.run()
