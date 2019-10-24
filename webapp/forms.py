from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('User password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Authorization', render_kw={"class": "btn btn-primary"})
