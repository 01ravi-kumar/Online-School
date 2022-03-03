from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from .models import *

views = Blueprint('views',__name__) # see flask documentation.


@views.route("/",methods=["GET","POST"])  # this '@views is the variable 'views' not the one inside the Blueprint.
@login_required
def home():        # we have created a blueprint. Now we need to register it in __init__.py file.
    std = Student.query.all()
    return render_template("home.html",user=current_user, students=std)


@views.route("/student/<var1>",methods=["GET", "POST"])
@login_required
def create_detail_student(var1):
    if var1=="create":
        if request.method=="POST":
            r_n,f_n,l_n=request.form["roll"],request.form["f_name"],request.form["l_name"]
            try:
                new_std=Student(roll_number=r_n,first_name=f_n,last_name=l_n)
                db.session.add(new_std)
                db.session.commit()
                return redirect(url_for('views.home'))

            except IntegrityError:
                db.session.rollback()
                flash('Student already exist. Use a different Roll Number',category="error")

        return render_template("create_student.html", user=current_user)

    elif var1.isdigit():
        std=Student.query.filter(Student.student_id == var1).first()
        en_list=db.session.query(Course.course_id,Course.course_code,Course.course_name,Course.course_description).join(Enrollments).filter(Enrollments.estudent_id==var1).all()
        return render_template("student_detail.html" , std=std, en_list=en_list, user=current_user)


@views.route("/student/<int:s_id>/withdraw/<int:c_id>",methods=["GET","POST"])
@login_required
def withdraw(s_id, c_id):
    Enrollments.query.filter(Enrollments.estudent_id == s_id, Enrollments.ecourse_id == c_id).delete()
    db.session.commit()
    return redirect(url_for('views.create_detail_student',var1=s_id))


@views.route("/student/<var1>/<var2>",methods=["GET","POST"])
@login_required
def update_delete_student(var1,var2):
    if var2 == "update":
        if request.method == "POST":

            f_n, l_n, c_id = request.form["f_name"], request.form["l_name"], request.form["course"]

            std = Student.query.filter(Student.student_id == var1).first()
            std.first_name = f_n
            std.last_name = l_n

            is_exist = Enrollments.query.filter(Enrollments.estudent_id==var1, Enrollments.ecourse_id==c_id).first()

            if not is_exist:
                er = Enrollments(estudent_id=var1, ecourse_id=c_id)
                db.session.add(er)
            db.session.commit()

            return redirect(url_for('views.home'))

        stu=Student.query.filter(Student.student_id==var1).first()
        cor=Course.query.all()
        return render_template("student_update.html",stu=stu,cor=cor,user=current_user)

    elif var2 == "delete":
        if request.method=="GET":
            std=Student.query.filter(Student.student_id==var1).delete()
            enroll=Enrollments.query.filter(Enrollments.estudent_id==var1).all()
            for er in enroll:
                db.session.delete(er)
            db.session.commit()
            return redirect(url_for('views.home'))


@views.route("/courses",methods=["POST","GET"])
@login_required
def courses():
    course_list = Course.query.all()
    return render_template('course.html',course_list=course_list,user=current_user)


@views.route("/course/<act>",methods=["POST","GET"])
@login_required
def create_detail_course(act):
    if request.method=="GET":
        if act=='create':
            return render_template("create_course.html",user=current_user)
        elif act.isdigit():
            course_detail = Course.query.filter(Course.course_id==act).first()
            enroll = db.session.query(Student.student_id,Student.roll_number,Student.first_name,Student.last_name).join(Enrollments).filter(Enrollments.ecourse_id==act).all()
            return render_template("course_detail.html",cou=course_detail,enroll=enroll,user=current_user)
    elif request.method == "POST":
        if act=="create":
            try:
                new_course=Course(course_code=request.form['code'],course_name=request.form['c_name'],course_description=request.form['desc'])
                db.session.add(new_course)
                db.session.commit()
                return redirect(url_for("views.courses"))
            except IntegrityError:
                db.session.rollback()
                flash("Course already exist. Create a different courser.",category="error")
                return render_template("create_course.html", user=current_user)


@views.route("/course/<c_id>/<act>",methods=["POST","GET"])
@login_required
def update_delete_course(c_id,act):
    if request.method=="GET":
        if act == "update":
            course_detail=Course.query.filter(Course.course_id == c_id).first()
            return render_template("course_update.html",cou=course_detail,user=current_user)
        elif act == "delete":
            course_detail = Course.query.filter(Course.course_id == c_id).first()
            db.session.delete(course_detail)
            db.session.commit()
            return redirect(url_for('views.courses'))

    if request.method=="POST":
        if act == "update":
            new_course=Course.query.filter(Course.course_id==c_id).first()
            new_course.course_name=request.form['c_name']
            new_course.course_description=request.form['desc']
            db.session.commit()
            return redirect(url_for("views.courses"))


@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html",user=current_user,img=url_for('static',filename='default.jpg'))
