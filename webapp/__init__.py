import boto3
from flask import Flask, render_template, request, redirect, Response
from flask_pagedown import PageDown
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
from werkzeug.utils import secure_filename
from webapp.upload_file_to_s3 import upload_file_to_s3
from webapp.filters import file_type
from webapp.filters import create_presigned_url


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'avi', 'mp4', 'mp3'])

app = Flask(__name__)
#Код ниже нужен для pagedown
app.config['SECRET_KEY'] = 'secret!'
pagedown = PageDown(app)
app.config.from_pyfile("config.py")
app.jinja_env.filters['file_type'] = file_type
app.jinja_env.filters['create_presigned_url'] = create_presigned_url

bucket = app.config["S3_BUCKET"]




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "user_file" not in request.files:
            return "No user_file key in request.files"
        file = request.files["user_file"]
        if file.filename == "":
            return "Please select a file"
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            upload_file_to_s3(file, bucket)
            my_bucket = get_bucket_from_s3()
            if my_bucket == None:
               return render_template('error.html') 
            else:
                summaries = my_bucket.objects.all()
                return render_template('main/main.html', files=summaries)
        else:
            return redirect("/")    
    else:
        my_bucket = get_bucket_from_s3()
        if my_bucket == None:
           return render_template('error.html') 
        else:    
            summaries = my_bucket.objects.all()
            return render_template('main/main.html', files=summaries)
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_bucket_from_s3():
    try:
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(bucket)
        return my_bucket
    except:
        return None    

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    my_bucket = get_bucket_from_s3()
    if my_bucket != None:
        my_bucket.Object(key).delete()
    return redirect('/')

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    my_bucket = get_bucket_from_s3()
    if my_bucket != None:
        file_obj = my_bucket.Object(key).get()
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )





#MainPage
#@app.route("/")
#@app.route("/main")
#def home():
#    return render_template('main/main.html')

#ChoiceCategory
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
def mark_down():
    form = PageDownFormExample()
    if form.validate_on_submit():
        text = form.pagedown
        # do something interesting with the Markdown text
    return render_template('category/mark_down_or_page_down.html', form = form)






if __name__ == "__main__":
    app.run(debug=True)