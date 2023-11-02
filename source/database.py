from sqlalchemy import create_engine, text   
from flask import *
from datetime import date
from source.funcs import *
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
    query = text("INSERT INTO users (email, pass, subscription, downloads, date) VALUES (:email, :password, :subscription,:downloads, :date)")

    conn.execute(query, 
                dict(email=data['email'], 
                password=str(sha256_crypt.hash(data['password'])), 
                subscription=0, 
                downloads=0,
                date=date.today())
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
            return str(data['email'])
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
# change Movie  status
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
# ---------------------------------------------
def lock_stat(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("UPDATE movies SET status = :status WHERE id = :id"),
                                  dict(status=0,
                                       id=id))
      return True
    except:
      print('Nothing Done to the database')
# ------------------------------------------ DELETE MOVIE FROM DATABASE USING ID
def delete_movie(id):
  with engine.connect() as conn:
    try: 
      update_status = conn.execute(text("DELETE FROM movies WHERE id =:id"),
                                   dict(id=id)) 
    except:
      print('Nothing Done to the database')
    