from flask import *
# from database import *
# from funcs import *
# import jwt
# import datetime 
# import os
from flask_cors import CORS 
from flask_bcrypt import Bcrypt
# from termcolor import colored

app = Flask(__name__)  # '__main__' 
Bcrypt(app)
CORS(app, support_credentials=True)


# The HomePage
@app.route('/')
def home_template(): 
    return render_template('index.html')
#  The Movies Page
@app.route('/movies')
def movie_template(): 
    return render_template('movies.html')
# The movie specific display
@app.route('/view')
def view_template(): 
    return render_template('view.html')


# ################################################
#  THIS IS THE ADMIN PANEL
# ###############################################
@app.route('/admin/dashboard')
def admin_home():
    return render_template('admin/index.html')
# users page
@app.route('/admin/users')
def admin_users():
    return render_template('admin/users.html')
# Sign a  new co-admin
@app.route('/admin/co-admin')
def co_admin():
    return render_template('admin/signup.html')
# Reviews Page
@app.route('/admin/reviews')
def user_reviews():
    return render_template('admin/reviews.html')
# manage a user page
@app.route('/admin/manage_user')
def manage_user():
    return render_template('admin/edit-user.html')
# add new item
@app.route('/admin/item')
def new_item():
    return render_template('admin/add-item.html')
# sign in co-admin
@app.route('/admin/login')
def login_coadmin():
    return render_template('admin/signin.html')
# Comments on users
@app.route('/admin/comments')
def comments():
    return render_template('admin/comments.html')
# wrong page
@app.route('/admin/404')
def invalid():
    return render_template('admin/404.html')
# Movie catalog page
@app.route('/admin/catalog')
def catalog():
    return render_template('admin/catalog.html')
# change password
@app.route('/admin/forgot')
def forgot():
    return render_template('admin/forgot.html')
















# For running the app
if __name__ == '__main__':
    app.run(debug=True)