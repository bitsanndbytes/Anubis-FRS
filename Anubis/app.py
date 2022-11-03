from concurrent.futures import thread
from flask import Flask, render_template, request, flash, session, url_for, redirect
import sqlite3
from functools import wraps
from werkzeug.utils import secure_filename
    #imports packages

app = Flask(__name__)
    #intiate flask app
app.secret_key='anubis'
    #app secret for flashing if password entered is incorrect


    # Used to Protect pages, unless user is logged in and session is stored.
def login_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        if session.get('username') is None:
            flash('You need to be logged in first!')
            return index()
        return f(*args, **kwargs)
    return login

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
    #Check for post and get messages from Login.html

        connection = sqlite3.connect('login.db')
        cursor = connection.cursor()
    #connects to the database called login.db which was created by login.py

        username = request.form['username']
    # gets the username typed in the login page
        password = request.form['password']
    # gets password typed in the login page
        print(username, password)
    #stores username as session cookie
        session['username'] = username
        

        querydb = "SELECT name,password FROM users where name= '"+username+"' and password='"+password+"'"
    # queries login.db to see if the username and password exists in login.db
        cursor.execute(querydb)

        answers = cursor.fetchall()
    #gets items in the database

        if len(answers) == 0:
            flash("Incorrect Username or Password!")
        else:
            return redirect(url_for("dashboard"))

    return render_template('Login.html')
    #displays login.html 

    #route for dashboard
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
     return render_template('dashboard.html')
    

    # Route for Training Faces
@app.route('/Upload', methods=['GET','POST'])
@login_required
def upload():
     return render_template('upload.html')   



    #route for logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    flash("You been Logged Out!")
    return redirect(url_for('index'))
    
    #route for notify
@app.route('/notify', methods=['GET','POST'])
@login_required
def notify():
    return render_template('notify.html')



if __name__ == '__main__':
    app.run(threaded=True)