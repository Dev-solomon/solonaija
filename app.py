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
















# For running the app
if __name__ == '__main__':
    app.run(debug=True)