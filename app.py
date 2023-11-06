from flask import *
from source.database import *
from source.funcs import *
import jwt
import datetime 
import os 
import sys
from flask_cors import CORS   
from termcolor import colored  


# ===================================|
app = Flask(__name__)  # '__main__'  |
CORS(app, support_credentials=True) #| 
# ===================================|


# The HomePage
@app.route('/')
def home_template(): 
    user = user_account()
    print(colored('Website has been visited!!!', 'yellow'))
    if user != '':
        return render_template('index.html', user=user)
    return render_template('index.html')
#  The Movies Page
@app.route('/movies')
@token_required
def movie_template(): 
    movies = get_movies()
    user = user_account()
    return render_template('movies.html', user=user, movies=movies)
# The movie specific display
@app.route('/view/<int:id>', methods=['GET','POST'])
@token_required
def view_template(id): 
    user = user_account() 
    movies = get_movies()
    movie = get_single_movie(id) 
    # send_file
    video = movie.vid
    comments = get_user_comments()  
    return render_template('view.html', user=user, comments=comments, ID=id, movies=movies, content=movie, video=video)
# Post the comment of a user
@app.route('/view/post_comment', methods=['POST','GET'])
@token_required
def post_comment(): 
    if request.method == 'POST':
        data = request.form
        comment = write_comment(data)
        if comment == True:
            return render_template('view.html', success="Comment Received!")
    else:
        return render_template('view.html')
# sign in 
@app.route('/login', methods=['GET','POST']) 
def login():
    if request.method == 'POST':
        data = request.form
        if login_user(data) == data['email']:
            user = data['email']
            if os.getenv('project') == 'development':
                token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 'solomon', 'HS256').decode('utf-8')
            else:
                token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 'solomon', 'HS256')
            print(colored(token, 'red')) #os.getenv('SECRET_KEY')
            print(type(token))
            return set_cookies(token)
        elif login_user(data) == 'admin':
            user = 'admin'
            if os.getenv('project') == 'development':
                token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 'solomon', 'HS256').decode('utf-8')
            else:
                token = jwt.encode({'user': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 'solomon', 'HS256')
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
@app.route('/logout_user', methods=['GET'])
def log_user_out():
    # User is logged out of the application
    return del_cookies()
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    


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
    users = get_users()
    if users != None:
        return render_template('admin/users.html', users=users)
    return render_template('admin/users.html')
# Reviews Page
@app.route('/admin/reviews')
@check_ifadmin
def user_reviews():
    return render_template('admin/reviews.html')
# add new item
@app.route('/admin/item', methods=['GET','POST'])
@check_ifadmin
def new_item():
    if request.method == 'POST': 
        data = request.form 
        image = upload_image()
        video = upload_video()  
        new_item = add_movie(data, image, video)
        if new_item == True:
            message = "New Movie Has Been Added"
            return render_template('admin/add-item.html', message=message)
    return render_template('admin/add-item.html') 
# Comments on users
@app.route('/admin/comments')
@check_ifadmin
def comments():
    comments = get_comments()
    if comments != None:
        return render_template('admin/comments.html', comments=comments)
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
    movies = get_movies()
    if movies != None:
        return render_template('admin/catalog.html', movies=movies)
    return render_template('admin/catalog.html')
# Change the stats of a movie
@app.route('/admin/<int:id>', methods=['POST','GET'])
def change_status(id):     
    change = change_stat(id)
    if change == True:
        movies = get_movies()
        return render_template('admin/catalog.html', movies=movies) 
#  Lock the movie 
@app.route('/lock/<int:id>', methods=['POST','GET'])
def lock_status(id):     
    change = lock_stat(id)
    if change == True:
        movies = get_movies()
        return render_template('admin/catalog.html', movies=movies)
#  Delete the movie from the catalog
@app.route('/admin/delete_movie/<int:id>', methods=["POST", 'GET'])
def delete_item(id):
    movie = delete_movie(id) 
    movies = get_movies()
    if movie == True:
        return render_template('admin/catalog.html', movies=movies, delete_mssg="Movie Has Been Deleted Successfully")
    return render_template('admin/catalog.html', movies=movies) 
# change password
# @app.route('/admin/forgot')
# @check_ifadmin
# def forgot():
#     return render_template('admin/forgot.html')
# Change the status of a user
@app.route('/admin/user/<int:id>', methods=['POST','GET'])
def change_user_status(id):     
    change = change_user_stat(id)
    if change == True:
        users = get_users()
        return render_template('admin/users.html', users=users) 
#  Lock the movie 
@app.route('/lock/user/<int:id>', methods=['POST','GET'])
def lock_user_status(id):     
    change = lock_user_stat(id)
    if change == True:
        users = get_users()
        return render_template('admin/users.html', users=users)
#  Delete the movie from the catalog
@app.route('/admin/delete_user/<int:id>', methods=["POST", 'GET'])
def delete_user(id):
    user= deleteuser(id) 
    users = get_users()
    if user == True:
        return render_template('admin/users.html', users=users, delete_mssg="User Deleted Successfully")
    return render_template('admin/users.html', users=users) 
# Change the status of a comment
@app.route('/admin/comment/<int:id>', methods=['POST','GET'])
def change_comment(id):     
    change = comment_stat(id)
    if change == True:
        comments = get_users()
        return render_template('admin/comments.html', comments=comments) 
#  Do not show the comment stated
@app.route('/lock/comment/<int:id>', methods=['POST','GET'])
def lock_this_comment(id):     
    change = lock_comment(id)
    if change == True:
        comments = get_comments()
        return render_template('admin/comments.html', comments=comments)
#  Delete the comment from the databse
@app.route('/admin/delete_comment/<int:id>', methods=["POST", 'GET'])
def deletecomment(id):
    comment = delete_comment(id) 
    comments = get_comments()
    if comment == True:
        return render_template('admin/comments.html', comments=comments, delete_mssg="Comment Deleted Successfully")
    return render_template('admin/comments.html', comments=comments) 

















# For running the app
if __name__ == '__main__':
    app.run(debug=True)