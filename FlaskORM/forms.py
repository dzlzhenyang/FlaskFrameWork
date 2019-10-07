import wtforms
from flask_wtf import FlaskForm
from wtforms import validators, ValidationError


def keywords_valid(form, field):
    """
    :param form: 表单
    :param field: 字段
    两个都不用主动传参
    """
    data = field.data
    keywords = ["admin", "管理员", "版主"]
    if data in keywords:
        raise ValidationError("不可以使用敏感词命名")


class TaskForm(FlaskForm):
    # label:任务名称
    name = wtforms.StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务名称"
        },
        # 校验字段
        validators={
            # DataRequired:空值校验
            validators.DataRequired("姓名不可以为空"),
            # Length：长度校验，需要量参数 min和max
            validators.Length(min=4, max=8),
            keywords_valid  # 直接添加，不用传参，默认传
        }
    )
    description = wtforms.TextField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务描述"
        },
        validators={
            # 判断两个字段是否相等，不相等error
            validators.EqualTo("name")
        }
    )
    time = wtforms.DateField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务时间"
        })
    public = wtforms.StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "公布任务人"
        })
