from flask import Blueprint

# 创建蓝图
main = Blueprint("main", __name__)

# 加载视图 加载整个views中的视图
from . import views
