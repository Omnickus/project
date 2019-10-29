from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from webapp.login.models import User
from webapp.login.forms import LoginForm
from webapp.db.db import db

blueprint = Blueprint('login', __name__)

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        title = 'Authorization'
        login_form = LoginForm()
        return render_template('login/login.html', form=login_form, title = title)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('index'))

