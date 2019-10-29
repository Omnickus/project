from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('User password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Authorization', render_kw={"class": "btn btn-primary", "style":"width:100%;"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()],
                              render_kw={"class": "form-control"})
    password2 = PasswordField('Retype the password', validators=[DataRequired(),
                               EqualTo('password')], render_kw={"class": "form-control"})   
    role = RadioField('Role', choices=[('admin','admin'), ('teacher','teacher'), ('student','student')],
                       default='student', validators=[DataRequired()],
                       render_kw={"class": "form-control", "class":"width480"})                                                                  
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary", "style":"width:100%;"})