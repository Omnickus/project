from flask import Flask, flash, Blueprint, render_template
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from webapp.db.db import db

from webapp.admin.views import blueprint as admin_blueprint

from webapp.category.views import blueprint as category_blueprint
from webapp.category.models import Category

from webapp.course.views import blueprint as course_blueprint
from webapp.course.models import Course

from webapp.lesson.views import blueprint as lesson_blueprint
from webapp.lesson.models import Lesson

from webapp.login.views import blueprint as login_blueprint
from webapp.login.models import User

from werkzeug.utils import secure_filename

from webapp.s3.filters import file_type
from webapp.s3.filters import create_presigned_url

#import sqlite3
#from getpass import getpass



def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.jinja_env.filters['file_type'] = file_type
    app.jinja_env.filters['create_presigned_url'] = create_presigned_url
    
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(course_blueprint)
    app.register_blueprint(lesson_blueprint)
    app.register_blueprint(login_blueprint)


    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/', methods=['GET'])
    def index():
        categories = Category.query.all()
        return render_template('index.html', categories=categories)
  
    return app