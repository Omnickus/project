from flask import Flask, render_template, request
from flask_pagedown import PageDown
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField




app = Flask(__name__)
#Код ниже нужен для pagedown
app.config['SECRET_KEY'] = 'secret!'
pagedown = PageDown(app)

#=============================Главная страница======================================
@app.route("/")
@app.route("/main")
def home():
    return render_template('main/main.html')

#====================Страница выбора категоии материала=============================
@app.route("/category")
def category():
    return render_template('category/category.html')
#Школьная программа------------------------
@app.route("/category/school")
def category_school():
    return render_template('category/school/school.html')
#Selenium ---------------------------------
@app.route("/category/selenium")
def selenium():
    return render_template('category/selenium.html')
#=========================Наши контакты=============================================
@app.route("/communication")
def communication():
    return render_template('communication/communication.html')
#=================PageDown==========================================================
class PageDownFormExample(FlaskForm):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')

@app.route('/category/mark_down_or_page_down', methods = ['GET', 'POST'])
def index():
    form = PageDownFormExample()
    if form.validate_on_submit():
        text = form.pagedown
        # do something interesting with the Markdown text
    return render_template('category/mark_down_or_page_down.html', form = form)






if __name__ == "__main__":
    app.run(debug=True)