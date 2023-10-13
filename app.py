from flask import *
from database import *
from funcs import *
import jwt
import datetime 
import os
from flask_bcrypt import Bcrypt
from flask_cors import CORS   
from termcolor import colored 


app = Flask(__name__)  # '__main__'  
CORS(app, support_credentials=True) 
bcrypt = Bcrypt(app) 


# The HomePage
@app.route('/')
def home_template(): 
    return render_template('index.html')
#  The Movies Page
@app.route('/movies')
@token_required
def movie_template(): 
    return render_template('movies.html')
# The movie specific display
@app.route('/view')
@token_required
def view_template(): 
    return render_template('view.html')
# sign in 
@app.route('/login', methods=['GET','POST']) 
def login():
    if request.method == 'POST':
        data = request.form
        if login_user(data) == data['email']:
            user = data['email']
            token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.getenv('SECRET_KEY'))
            return set_cookies(token)
        elif login_user(data) == 'admin':
            user = 'admin'
            token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.getenv('SECRET_KEY'))
            return set_cookies(token)
        return  render_template('admin/signin.html', message="Email Or Password Incorrect")
    else:
        return render_template('admin/signin.html') 
# Signup
@app.route('/signup', methods=['GET','post'])
def co_admin():
    if request.method == 'POST':
        data = request.form
        registration(data)   
        return render_template('admin/signin.html', info="Successfully Registered, Login!") 
    else:
        return render_template('admin/signup.html')


# ################################################
#  THIS IS THE ADMIN PANEL
# ###############################################
@app.route('/admin/dashboard')
@check_ifadmin
def admin_home():
    return render_template('admin/index.html')
# users page
@app.route('/admin/users')
@check_ifadmin
def admin_users():
    return render_template('admin/users.html')
# Reviews Page
@app.route('/admin/reviews')
@check_ifadmin
def user_reviews():
    return render_template('admin/reviews.html')
# manage a user page
@app.route('/admin/manage_user')
@check_ifadmin
def manage_user():
    return render_template('admin/edit-user.html')
# add new item
@app.route('/admin/item', methods=['GET','POST'])
@check_ifadmin
def new_item():
    if request.method == 'POST': 
        pass 
    # for file in os.listdir('static/upload'):
    #     print(file)  
    return render_template('admin/add-item.html')
# -------------------------------------------
@app.route('/admin/upload', methods=['POST'])
def Upload():
    return upload_image()
# Comments on users
@app.route('/admin/comments')
@check_ifadmin
def comments():
    return render_template('admin/comments.html')
# wrong page
@app.route('/admin/404')
@check_ifadmin
def invalid():
    return render_template('admin/404.html')
# Movie catalog page
@app.route('/admin/catalog')
@check_ifadmin
def catalog():
    return render_template('admin/catalog.html')
# change password
@app.route('/admin/forgot')
@check_ifadmin
def forgot():
    return render_template('admin/forgot.html')
















# For running the app
if __name__ == '__main__':
    app.run(debug=True)