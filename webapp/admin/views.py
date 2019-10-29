from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from webapp.db.db import db
from webapp.login.decorators import admin_required
from webapp.login.models import User
from webapp.login.forms import RegistrationForm

blueprint = Blueprint('admin', __name__)

@blueprint.route('/admin')
@login_required
def admin_index():
    print(current_user)
    if current_user.is_admin:
        return('Привет админ')
    else:
        return('Ты не админ')
   
@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        title = "Registration"
        is_homepage = False
        is_loginpage = False
        is_catalogpage = False
        is_adminpage = False
        is_registrationpage = True
        form = RegistrationForm()
        return render_template('admin/registration.html', page_title=title, is_homepage=is_homepage,
                                is_loginpage=is_loginpage, is_catalogpage=is_catalogpage,
                                is_adminpage=is_adminpage, is_registrationpage=is_registrationpage,
                                form=form)
    elif request.method == 'POST': 
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, role=form.role.data)
            if User.query.filter(User.username == form.username.data).count():
                flash('Имя занято')
                return redirect(url_for('admin.registration'))
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('The user ' + new_user.username + ' was created successfully.')
            return redirect(url_for('admin.admin_index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Error in the field "{}":  {}'.format(getattr(form, field).label.text, error))
            return redirect(url_for('admin.registration'))
    else:
        return redirect('/')


'''       
@blueprint.route('/registration')
def registration():
    return render_template('admin/registration.html')
'''
'''
@blueprint.route('/registration', methods = ['POST', 'GET'], )
def registration():
    username = request.form['login']
    role = request.form['gender']
    if User.query.filter(User.username == username).count():
        return 'Имя используется'

    password_1 = request.form['password_1']
    password_2 = request.form['password_2']
    if not password_1 == password_2:
        return 'Пароли не совпадают'

    new_user = User(username=username, role= role )
    new_user.set_password(password_1)

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index', role = role))
      '''   