from app import create, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create()
manage = Manager(app)
migrate = Migrate(app, models)
app.secret_key = "123"
manage.add_command("db", MigrateCommand)
# 添加一条命令
# @manage.command
# def migrate():
#     models.create_all()


if __name__ == '__main__':
    # flask自带的启动项目的命令 shell,runserver
    manage.run()
