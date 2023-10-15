from sqlalchemy import create_engine, text   
from flask import *
from datetime import date
from funcs import *
from termcolor import colored
from flask_bcrypt import Bcrypt
from app import app
bcrypt = Bcrypt(app)
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
                password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
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
        if row._mapping['email'] == data['email'] and  bcrypt.check_password_hash(row._mapping['pass'], data['password']): 
          return data['email']
    if data['email'] == "ntiasolomon9@gmail.com" and data['password'] == "123":
        return 'admin'
    return None
#------------------------------------------ 
# add a new movie to database 
# -----------------------------------------
# def add_movie(image, video):
#   with engine.connect() as conn:
#     result = 