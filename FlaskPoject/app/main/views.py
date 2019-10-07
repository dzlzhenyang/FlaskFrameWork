import os
import datetime
import json
import hashlib
import functools

from flask import render_template, request, redirect, session, jsonify
from flask_restful import Resource

from . import main
from app import api
from app.models import *
from .forms import TaskForm
# from main import csrf

from settings import STATICFILES_DIR
# 调用日历
from ..common_code.get_calendar import Calendar
from ..common_code.get_page import Paginator


def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def login_valid(func):
    # 保留原函数的名称，不让它变成inner，flask中需要这样，是因为视图和url在同一个文件中
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # 获取cookie
        cookie_username = request.cookies.get("username")
        # 获取session
        session_username = session.get("username")
        # 获取字典get 可以有多个参数
        id = request.cookies.get("user_id", "0")
        # 查询时，get只能有一个参数
        user = User.query.get(int(id))
        if user and cookie_username == user.username and session_username == cookie_username:
            return func(*args, **kwargs)
        else:
            return redirect("/login/")

    return inner


@main.route("/register/", methods=["GET", "POST"])
# @csrf.exempt
def register():
    error_message = ""
    if request.method == "POST":
        # 接收前端传来的name参数
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        r_password = request.form.get("r_password")
        if password != r_password:
            error_message = "两次输入密码不一致，请重新输入"
        else:
            # 判断用户名和邮箱是否输入
            if username and email:
                # 查看数据库中同名的username
                user = User.query.filter_by(username=username).first()
                # 如果数据库中没有，就新建一个user，添加注册的数据
                if not user:
                    new_user = User()
                    new_user.username = username
                    new_user.email = email
                    new_user.password = set_password(password)
                    new_user.save()
                else:
                    error_message = "用户名已经被注册！"
            else:
                error_message = "邮箱或用户名不能为空"

    return render_template("register.html", **locals())


@main.route("/login/", methods=["get", "post"])
# @csrf.exempt
def login():
    error_message = ""
    if request.method == "POST":
        # 通过form表单获取前端传来的数据
        username = request.form.get("username")
        password = request.form.get("password")
        if username:
            # 根据username获取数据库的一条user信息
            user = User.query.filter_by(username=username).first()
            # 如果可以获取到
            if user:
                # 对password进行加密
                password = set_password(password)
                # 判断两者密码是否一致
                if password == user.password:
                    # 一致的话进入首页
                    response = redirect("/index/")
                    # 设置cookie username和user_id
                    response.set_cookie("username", user.username)
                    response.set_cookie("user_id", str(user.id))
                    # 设置session username
                    session["username"] = user.username
                    return response
                else:
                    error_message = "密码错误"
            else:
                error_message = "用户名不存在"
        else:
            error_message = "用户名不能为空"
    return render_template("login.html", **locals())


@main.route("/logout/")
def logout():
    response = redirect("/login/")
    # 删除cookie
    response.delete_cookie("username")
    response.delete_cookie("user_id")
    # 删除session
    del session["username"]
    return response


@main.route("/index/")
@login_valid
def index():
    return render_template("index.html")


@main.route("/user_info/")
@login_valid
def user_info():
    """
    完善日历和课程表的功能
    """
    # 实例化课程表对象
    calendar = Calendar()
    # 返回结果才是一个列表嵌套列表的日历
    result = calendar.return_calendar()
    return render_template("user_info.html", **locals())


@main.route("/application_for_leave/", methods=["get", "post"])
@login_valid
def application_for_leave():
    """
    请假条申请
    """
    if request.method == "POST":
        # 获取前端传来的数据
        person_name = request.form.get("person_name")
        person_phone = request.form.get("person_phone")
        leave_type = request.form.get("leave_type")
        leave_description = request.form.get("leave_description")
        leave_start_time = request.form.get("leave_start_time")
        leave_end_time = request.form.get("leave_end_time")

        # 实例化请假条对象
        afl = ApplicationForLeave()
        # 将数据保存到数据库中
        afl.person_id = request.cookies.get("user_id")
        afl.person_name = person_name
        afl.person_phone = person_phone
        afl.leave_type = leave_type
        afl.leave_description = leave_description
        afl.leave_start_time = leave_start_time
        afl.leave_end_time = leave_end_time
        afl.leave_status = "0"
        afl.save()
    return render_template('application_for_leave.html', **locals())


@main.route("/leave_list/<int:page>/")
@login_valid
def leave_list(page):
    """
    请假条列表
    :param page: 页码
    """
    afl = ApplicationForLeave.query.all()
    # 传入数据  每页数据为3条
    paginator = Paginator(afl, 4)
    page_data = paginator.page_data(page)
    return render_template("leave_list.html", **locals())


# def leave_list(page):
#     # 0页  1-5
#     # 1页  6-10
#     # 2页  11-15
#     id = int(request.cookies.get("id"))
#     offsetnum = (page - 1) * page_num
#     leaves = Leave.query.filter_by(request_id=id).order_by(models.desc("id"))  # 获取该用户所有假条
#     page_total = math.ceil(leaves.count()/page_num)  # 总页数
#     page_list = range(1,page_total+1)  # 页表页码
#
#     leaves = leaves.offset(offsetnum).limit(page_num) # 获取当前页的数据
#     return render_template("leave_list.html", **locals())


@main.route("/add_task/", methods=['get', 'post'])
def add_task():
    errors = ""
    task = TaskForm()
    if request.method == "POST":
        # 判断一个是否是有效的post请求
        if task.validate_on_submit():
            form_data = task.data
        else:
            errors = task.errors
    return render_template("add_task.html", **locals())


@main.route("/picture/", methods=["get", "post"])
def picture():
    picture = {"picture": "img/1111.jpg"}
    if request.method == "POST":
        # 保存到服务器
        file = request.files.get("photo")
        file_name = file.filename
        file_path = "img/%s" % file_name
        save_path = os.path.join(STATICFILES_DIR, file_path)
        file.save(save_path)

        # 保存到数据库
        picture = Picture()
        picture.picture = file_path
        picture.save()
    return render_template("picture.html", **locals())


@api.resource("/Api/leave/")
class LeaveApi(Resource):
    # 定义返回的格式
    def __init__(self):
        super(LeaveApi, self).__init__()
        self.result = {
            "version": "1.0",
            "method": "",
            "data": ""
        }

    # get版本1
    # def get(self):
    #     if request.method == "GET":
    #         self.result["method"] = "GET"
    #         data = request.args
    #         id = data.get("id")
    #         if id:
    #             afl = ApplicationForLeave.query.get(int(id))
    #             result_data = {
    #                 "person_id": afl.person_id,
    #                 "person_name": afl.person_name,
    #                 "person_phone": afl.person_phone,
    #                 "leave_type": afl.leave_type,
    #                 "leave_description": afl.leave_description,
    #                 "leave_start_time": afl.leave_start_time,
    #                 "leave_end_time": afl.leave_end_time
    #             }
    #             self.result["data"] = result_data
    #         else:
    #             afl = ApplicationForLeave.query.all()
    #             result_data = []
    #             for i in afl:
    #                 result = {
    #                     "person_id": i.person_id,
    #                     "person_name": i.person_name,
    #                     "person_phone": i.person_phone,
    #                     "leave_type": i.leave_type,
    #                     "leave_description": i.leave_description,
    #                     "leave_start_time": i.leave_start_time,
    #                     "leave_end_time": i.leave_end_time
    #                 }
    #                 result_data.append(result)
    #             self.result["data"] = result_data
    #
    #     return self.result
    def get_data(self, afl):  # 获取数据
        result_data = {
            "person_id": afl.person_id,
            "person_name": afl.person_name,
            "person_phone": afl.person_phone,
            "leave_type": afl.leave_type,
            "leave_description": afl.leave_description,
            "leave_start_time": afl.leave_start_time,
            "leave_end_time": afl.leave_end_time
        }
        return result_data

    # get优化
    def get(self):
        data = request.args
        id = data.get("id")
        if id:
            afl = ApplicationForLeave.query.get(int(id))
            if afl:
                result_data = self.get_data(afl)
            else:
                result_data = "查询失败，id为%s的数据不存在" % id
        else:
            afl = ApplicationForLeave.query.all()
            result_data = []
            for i in afl:
                result_data.append(self.get_data(i))
        self.result["data"] = result_data
        self.result["method"] = "GET"
        return self.result

    def post(self):  # 用来保存数据
        data = request.form
        afl = ApplicationForLeave()
        afl.person_id = data.get("person_id")
        afl.person_name = data.get("person_name")
        afl.person_phone = data.get("person_phone")
        afl.leave_type = data.get("leave_type")
        afl.leave_description = data.get("leave_description")
        afl.leave_start_time = data.get("leave_start_time")
        afl.leave_end_time = data.get("leave_end_time")
        afl.leave_status = "0"
        afl.save()
        self.result["data"] = self.get_data(afl)
        self.result["method"] = "POST"
        return self.result

    # 对数据进行修改
    # def put(self):  # 方法1
    #     data = request.form
    #     id = data.get("id")
    #     afl = ApplicationForLeave.query.get(int(id))
    #     if afl:
    #         # 传来的数据修改的就修改，不修改的就为原来的数据
    #         afl.person_id = data.get("person_id", afl.person_id)
    #         afl.person_name = data.get("person_name", afl.person_name)
    #         afl.person_phone = data.get("person_phone", afl.person_phone)
    #         afl.leave_type = data.get("leave_type", afl.leave_type)
    #         afl.leave_description = data.get("leave_description", afl.leave_description)
    #         afl.leave_start_time = data.get("leave_start_time", afl.leave_start_time)
    #         afl.leave_end_time = data.get("leave_end_time", afl.leave_end_time)
    #         afl.save()
    #         self.result["data"] = self.get_data(afl)
    #         self.result["method"] = "PUT"
    #     else:
    #         self.result["data"] = "修改失败，id为%s的数据不存在" % id
    #
    #     return self.result

    def put(self):  # 方法2
        data = request.form
        id = data.get("id")
        afl = ApplicationForLeave.query.get(int(id))
        if afl:
            # print(data.__dict__)
            for key, value in data.items():
                print(key, value)
                # 不对id进行修改
                if key != "id":
                    # 只修改变更的数据
                    setattr(afl, key, value)
            afl.save()
            self.result["data"] = self.get_data(afl)
            self.result["method"] = "PUT"
        else:
            self.result["data"] = "修改失败，id为%s的数据不存在" % id
        return self.result

    def delete(self):
        data = request.form
        id = data.get("id")
        afl = ApplicationForLeave.query.get(int(id))
        if afl:
            afl.delete()
            self.result["data"] = "删除成功！id为%s的数据被成功删除" % id
            self.result["method"] = "DELETE"
        else:
            self.result["data"] = "删除失败，id为%s的数据不存在"
        return self.result
