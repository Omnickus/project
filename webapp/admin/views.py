from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from webapp.db.db import db
#from webapp.login.decorators import admin_required
from webapp.login.models import User

blueprint = Blueprint('admin', __name__)

@blueprint.route('/admin')
@login_required
def admin_index():
    print(current_user)
    if current_user.is_admin:
        return('Привет админ')
    else:
        return('Ты не админ')
        
