from flask import Blueprint, redirect,render_template, request
from flask_login import login_required, current_user
from sqlalchemy import exc
from webapp.category.models import Category
from webapp.course.models import Course
from webapp.db.db import db

blueprint = Blueprint('category', __name__)

@blueprint.route('/categories', methods=['POST'])
@login_required
def add_a_category():
    try:
        name = request.form['category']
        new_category = Category(name)
        if new_category.name != '':
            db.session.add(new_category)
            db.session.commit()
    except(exc.IntegrityError):
        print('the category exists')
        return redirect('/')     
    return redirect('/')                 


@blueprint.route('/delete_a_category', methods=['POST'])
@login_required
def delete_a_category():
    try:
        category_id = request.form['category_id']
        category_delete = Category.query.filter_by(id=category_id).delete()
        db.session.commit() 
    except:
        return redirect('/')    
    return redirect('/') 

@blueprint.route('/<link_path>', methods=['GET', 'POST'])
@login_required
def page(link_path):
    category_exists = Category.query.filter_by(name=link_path).first()
    if category_exists:
        if request.method == 'POST':
            try:
                name = request.form['course']
                course_description = 'This is the best course'
                new_course = Course(name, category_exists.id, course_description)              
                if new_course.name != '':
                    db.session.add(new_course)
                    db.session.commit()
            except(exc.IntegrityError):
                print('the course exists')
            return redirect('/'+link_path) 
        else:
            courses = Course.query.filter(Course.category_id==category_exists.id).all()    
            return render_template('category/category.html', category_name=link_path, courses=courses)  
    else:
        return render_template('error.html')         
