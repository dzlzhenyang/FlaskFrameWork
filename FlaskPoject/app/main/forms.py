import wtforms
from flask_wtf import FlaskForm
from wtforms import validators, ValidationError


# 自定义的校验
def keywords_valid(form, field):
    """
        :param form: 表单
        :param field:  字段
        这两个都不用主动传参
        """
    data = field.data
    keywords = ["admin", "管理员", "版主"]
    if data in keywords:
        raise ValidationError("不可以使用敏感词命名")


# 设置任务校验
class TaskForm(FlaskForm):
    # 任务名称
    name = wtforms.StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务名称"
        },
        # 校验字段
        validators={
            # DataRequired:空值校验
            validators.DataRequired("姓名不能为空"),
            # Length：长度检验 需要两个参数max和min
            validators.Length(max=8, min=4),
            # 添加自定义校验 不需要传参
            keywords_valid
        }
    )
    # 任务描述
    description = wtforms.TextField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务描述"
        },
        validators={
            # EqualTo：判断两个字段是否相等，不相等error
            validators.EqualTo("name")
        }
    )
    # 任务时间
    time = wtforms.DateField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务时间"
        })
    # 公布任务人
    public = wtforms.StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "公布任务人"
        })
