from flask import *
import jwt
from functools import wraps
import os  
from termcolor import colored
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage 
# -----------------------------------------------
# This is the function for tokens' acccessibility
# -----------------------------------------------
def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.cookies.get('token') 

    if not token:
      return render_template('admin/signin.html', message="Sorry! You're Not Authorized")
    
    try:
      data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])  
    except:
      return  render_template('admin/signin.html', message="Session Expired! Login")
    
    return f(*args, **kwargs)  
  return decorated 
# ------------------------------------
# Function for setting cookies 
# ------------------------------------
def set_cookies(token):
  checked_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
  if checked_token['user'] == 'admin':
    resp = make_response(redirect(url_for('admin_home'))) 
    resp.set_cookie('token', str(token))
    return resp
  resp = make_response(redirect(url_for('home_template'))) 
  resp.set_cookie('token', str(token))
  return resp
# --------------------------------------------------
# Function for Deleting cookie and Logging User Out
# --------------------------------------------------
def del_cookies():
    resp = make_response(render_template('admin/signin.html')) 
    resp.delete_cookie('token')
    return resp
# ------------------------------------------------------------
# Function for Getting Who the user in on dashboard
# ------------------------------------------------------------
def user_account():
    token = request.cookies.get('token') 
    
    try:
      data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
      return data
    except:
      return  render_template('admin/signin.html', message="oops! something went wrong")
# ------------------------------------------------------------
# Function for Uploading Images and videos
# ------------------------------------------------------------
def upload_image():
  image = request.files['cover']
  if image.filename != '':
      image.save(os.path.join('static/upload/', secure_filename(image.filename))) 
      return image.filename
  return None

# ALLOWED_EXTENSIONS = ['mp4']

# def allowed_file(filename):
#   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_video():
  if 'movie' not in request.files:
    return 'No video file found!'
  video = request.files['movie']
  if video.filename == '':
    return 'No video selected'
  if video :
    video.save(os.path.join('static/videos/', secure_filename(video.filename)))
    return video.filename
# -----------------------------------------------
# Function to give Admins accessibility to panel
# -----------------------------------------------
def check_ifadmin(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    url= request.method
    try:
      if url == 'GET':
        token = request.cookies.get('token')
        data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"]) 
    except:
      return render_template('admin/signin.html', message="SESSION EXPIRED! LOGIN")
    
    token = request.cookies.get('token')
    data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])    
    if data['user'] != 'admin':
      return render_template('admin/404.html', message="ACCESS DENIED!")
    
    return f(*args, **kwargs)  
  return decorated  
  
  