from concurrent.futures import thread
from flask import Flask, render_template, request, flash, session, url_for, redirect, Response
import sqlite3
import os 
import cv2
from functools import wraps
from werkzeug.utils import secure_filename
import threading
import multiprocessing
    #imports packages

global camera2
global camera1

    #save camera variable as file
def savevar(camname):
    file = open("cameraurl.txt", "a")
    str1 = repr(camname)
    file.write(f""+ camname + "\n")
    file.close()


app = Flask(__name__)
    #intiate flask app
app.secret_key='anubis'
    #app secret for flashing if password entered is incorrect
app.config['UPLOAD_FOLDER'] ="static\Faces"
    #upload folder for images

    # Used to Protect pages, unless user is logged in and session is stored.
def login_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        if session.get('username') is None:
            flash('You need to be logged in first!')
            return index()
        return f(*args, **kwargs)
    return login
    # to capture frames from user input might also be using for facial recognition
def gen_frames(y):
    cam1 = cv2.VideoCapture(y)
    cam1.set(cv2.CAP_PROP_FPS, 60)
    while True:
        success, frame = cam1.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # to capture frame 2 of user input might also be used for facial recognition
def frames(x):
    cam2 = cv2.VideoCapture(x)
    cam2.set(cv2.CAP_PROP_FPS, 60)
    while True:
        success, frame = cam2.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # route stream to dashboard using multipart -x 
@app.route('/stream1')
def stream1():
    return Response(frames(x=camera2),mimetype='multipart/x-mixed-replace; boundary=frame')
    # route stream to dashboard using multipart
@app.route('/stream')
def stream():
    return Response(gen_frames(y=camera1),mimetype='multipart/x-mixed-replace; boundary=frame')


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
    if request.method == 'POST':
        try: 
            global camera1
            global camera2
            camera2 = request.form['camera2']
            savevar(camera2)
            frames(camera2)
        except:
            if request.method == 'POST':
                camera1 = request.form['camera1']
                savevar(camera1)
                gen_frames(camera1)
    return render_template('dashboard.html')
    

    # Route for Training Faces
@app.route('/Upload', methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'POST':
    # File uploaded from Upload.html
        image = request.files['Recimage']
    # Name of Person From Upload.html
        text = request.form['Recusername']
    # If user submits empty file or and empty person's name
        if image.filename == '' or text == '':
            flash('No Image Uploaded, Try Again')
            return render_template('upload.html')
    # if image is uploaded, save the image to the Faces Folder
        if image == request.files['Recimage']:
    # Renames the file to the Person's Name
            image.filename = str(text) + '.jpg'
            save = secure_filename(image.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], save)
            image.save(path)

            #text = request.form['Recuser']
            flash('Image was uploaded succesfully!')
            
            return render_template('upload.html')
    return render_template('upload.html')   


    #route for notify
@app.route('/notify', methods=['GET','POST'])
@login_required
def notify():
    return render_template('notify.html')


    #route for logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    flash("You have been Logged Out!")
    return redirect(url_for('index'))
    




if __name__ == '__main__':
    app.run(threaded=True)   
    p = threading.Thread(target=gen_frames(), args=())
    p.daemon = True
    p.start()
    gen = threading.Thread(target=frames(), args=())
    gen.start()
    gen.daemon = True
    p1 = multiprocessing.Process(target=gen_frames(), args=())
    p1.start()
    p2 = multiprocessing.Process(target=frames(), args=())
    p2.start()