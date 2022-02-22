from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    designation = db.Column(db.String)
    department = db.Column(db.String)
    email = db.Column(db.String,nullable=False, unique=True)
    password = db.Column(db.String,nullable=False)


    def get_id(self):
        return self.user_id

class Student(db.Model):
    __tablename__='student'
    student_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    roll_number = db.Column(db.String,unique=True,nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer , primary_key=True,autoincrement=True)
    course_code = db.Column(db.String,unique=True,nullable=False)
    course_name = db.Column(db.String,nullable=False)
    course_description = db.Column(db.String)


class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    estudent_id = db.Column(db.Integer,db.ForeignKey("student.student_id"),nullable=False)

    ecourse_id = db.Column(db.Integer,db.ForeignKey("course.course_id"),nullable=False)