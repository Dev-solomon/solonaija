from sqlalchemy import create_engine, text   
from flask import *
from datetime import date
from source.funcs import *
import sys
from termcolor import colored  
from passlib.hash import sha256_crypt
# ----------------------------------------------------------
# Connection string For Cloud connection to Database
# ----------------------------------------------------------
connection_string= "mysql+pymysql://ek8as402ht1fx4v994tt:pscale_pw_rrZJhA3U4Qfm5yyqSPbBU8t4Mle2wK6UW8V7A8ftGc@aws.connect.psdb.cloud/solonaija?charset=utf8mb4"
# ******************************************************
engine = create_engine(
  connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }) 
# --------------------------------------------------------------
# This is the function to add users and their whole basic info
# --------------------------------------------------------------
def registration(data):
  with engine.connect() as conn:
    query = text("INSERT INTO users (email, pass, subscription, downloads, date, status) VALUES (:email, :password, :subscription,:downloads, :date, :status)")

    conn.execute(query, 
                dict(email=data['email'], 
                password=sha256_crypt.hash(data['password']), 
                subscription=0, 
                downloads=0,
                date=date.today(),
                status=1)
                ) 
    print('{} Sucessfully Registered'.format(data['email']))
#------------------------------------------ 
# The login function for users  
# -----------------------------------------
def login_user(data):
  with engine.connect() as conn:
    result = conn.execute(text("select * from users"))
    
    # users = []
    for row in result.fetchall():  
        if row._mapping['email'] == data['email']:
          if sha256_crypt.verify(data['password'], row._mapping['pass']):
            return data['email']
          else:
            return False
    if data['email'] == "ntiasolomon9@gmail.com" and data['password'] == "123":
        return 'admin'
    return None
# ------------------------------------------ 
# add a new movie to database 
# -----------------------------------------
def add_movie(data, image, video):
  with engine.connect() as conn:
    result = text("INSERT INTO movies (title, description, year, timewatch, genre, image, vid, status, date) VALUES (:title, :description, :year, :timewatch, :genre, :image, :vid, :status, :date)")
    
    conn.execute(result,
                 dict(
                   title=data['title'],
                   description=data['desc'],
                   year=data['year'],
                   timewatch=data['timeplay'],
                   genre=data['genre'],
                   image=image,
                   vid=video,
                   status=0,
                   date=date.today()
                 ))
    print(f"{data['title']} has been sucessfully added to the Database.")
    return True
# ------------------------------------------ 
# View the catalog movie database 
# -----------------------------------------
def get_movies():
  with engine.connect() as conn:
    query = text("SELECT * FROM movies")
    movies = conn.execute(query).fetchall()
    if len(movies) == 0:
      return None
    else: 
      return movies
# ------------------------------------------ 
# change Movie  status TO VIEWABLE
# -----------------------------------------
def change_stat(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("UPDATE movies SET status = :status WHERE id = :id"),
                                  dict(status=1,
                                       id=id))
      return True
    except:
      print('Nothing Done to the database')
# ----------------------------------------
# LOCK MOVIE FROM BEING VIEWED
# ----------------------------------------
def lock_stat(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("UPDATE movies SET status = :status WHERE id = :id"),
                                  dict(status=0,
                                       id=id))
      return True
    except:
      print('Nothing Done to the database')
# ----------------------------------------
# DELETE MOVIE FROM DATABASE USING ID
# ----------------------------------------
def delete_movie(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("DELETE FROM movies WHERE id =:id"),
                                   dict(id=id)) 
      return True
    except:
      print('Nothing Done to the database')
#------------------------------------------ 
# Get all users from the database
# -----------------------------------------
def get_users():
  with engine.connect() as conn:
    query = text("SELECT * FROM users")
    users = conn.execute(query).fetchall()
    if len(users) == 0:
      return None
    else: 
      return users
# ------------------------------------------ 
# CHANGE THE STATUS OF THE USER TO ACTIVE
# -----------------------------------------
def change_user_stat(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("UPDATE users SET status = :status WHERE id = :id"),
                                  dict(status=1,
                                       id=id))
      return True
    except:
      print(colored('User status not been activated', 'red'))
# -----------------------------------------------
# LOCK USER | DISABLE THE USER FROM BEING ACTIVE
# -----------------------------------------------
def lock_user_stat(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("UPDATE users SET status = :status WHERE id = :id"),
                                  dict(status=0,
                                       id=id))
      return True
    except:
      print(colored('User status not deactivated', 'red'))
# ----------------------------------------
# DELETE USER FROM DATABASE USING ID
# ----------------------------------------
def deleteuser(id):
  with engine.connect() as conn:
    try: 
      user = conn.execute(text("DELETE FROM users WHERE id =:id"),
                                   dict(id=id)) 
      return True
    except:
      print(colored("Attempt to delete user failed!", 'red'))
#------------------------------------------ 
# GET COMMENTS FROM THE DATABASE
# -----------------------------------------
def get_comments():
  with engine.connect() as conn:
    query = text("SELECT * FROM comments")
    comments = conn.execute(query).fetchall()
    if len(comments) == 0:
      return None
    else: 
      return comments
# ------------------------------------------ 
# CHANGE THE STATUS OF THE COMMENT TO ACTIVE
# -----------------------------------------
def comment_stat(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("UPDATE comments SET status = :status WHERE id = :id"),
                                  dict(status=1,
                                       id=id))
      return True
    except:
      print(colored('Comment not activated', 'red'))
# --------------------------------------------------
# LOCK USER | DISABLE THE COMMENT FROM BEING ACTIVE
# --------------------------------------------------
def lock_comment(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("UPDATE comments SET status = :status WHERE id = :id"),
                                  dict(status=0,
                                       id=id))
      return True
    except:
      print(colored('Comment not deactivated', 'red'))
# ----------------------------------------
# DELETE COMMENT FROM DATABASE USING ID
# ----------------------------------------
def delete_comment(id):
  with engine.connect() as conn:
    try: 
      comment = conn.execute(text("DELETE FROM comments WHERE id =:id"),
                                   dict(id=id)) 
      return True
    except:
      print(colored("Attempt to delete user failed!", 'red'))
# ----------------------------------------
# USER CAN WRITE A COMMENT
# ----------------------------------------
def write_comment(data):
  with engine.connect() as conn:
    try:
      user = user_account()['user'] #The current user of the account
      query = text("INSERT INTO comments (author, comments, date, status) VALUES (:author, :comments, :date, :status)")
      make_comment = conn.execute(query, dict(
        author=user,
        comments=data['comm'],
        date=date.today(),
        status=0
      ))
      print("Comment made sucessfully")
      return True
    except:
      print(colored("something wrong somewhere", 'yellow'))
      return False
#------------------------------------------ 
# GET COMMENTS TO DISPLAY FOR USERS
# -----------------------------------------
def get_user_comments():
  with engine.connect() as conn:
    query = text("SELECT * FROM comments WHERE status = 1 LIMIT 4")
    comments = conn.execute(query).fetchall()
    if len(comments) == 0:
      return None
    else: 
      return comments
#------------------------------------------ 
# FETCH FOR A SINGLE MOVIE
# -----------------------------------------
def get_single_movie(ID):
  with engine.connect() as conn:
    query = text("SELECT * FROM movies WHERE id = :id")
    single_movie = conn.execute(query, dict(id=ID)).fetchall()
    if len(single_movie) == 0:
      return None
    else: 
      return single_movie[0]