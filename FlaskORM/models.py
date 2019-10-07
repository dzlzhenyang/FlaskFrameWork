from main import models


class BaseModel(models.Model):
    __abstract__ = True  # 声明当前类是抽象类，被继承调用而不被创建
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db = models.session()
        db.add(self)
        db.commit()

    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()


# 课程表
class Course(BaseModel):
    __tablename__ = "course"
    course_number = models.Column(models.String(32))
    course_name = models.Column(models.String(32))
    course_time = models.Column(models.Date)
    course_teacher = models.Column(models.String(32))


# 用户表
class User(BaseModel):
    __tablename__ = "user"
    username = models.Column(models.String(32))
    email = models.Column(models.String(32))
    password = models.Column(models.String(32))


# 请假条表
class ApplicationForLeave(BaseModel):
    """
       申请  0
       批准  1
       驳回  2
       销假  3
       """
    __tablename = "application_for_leave"
    person_id = models.Column(models.String(32))
    person_name = models.Column(models.String(32))
    person_phone = models.Column(models.String(32))
    leave_type = models.Column(models.String(32))
    leave_description = models.Column(models.Text)
    leave_start_time = models.Column(models.String(32))
    leave_end_time = models.Column(models.String(32))
    leave_status = models.Column(models.Integer)


class Picture(BaseModel):
    __tablename__ = "picture"
    picture = models.Column(models.String(64))
