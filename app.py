from flask import Flask, render_template, request, redirect, url_for, Response
from flask_restful import Resource, Api
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
# from database import Sessionlocal, engine
from models import Image
from flask import request, session, send_from_directory
from werkzeug.utils import secure_filename
from database import db_init, db
from models import Image

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_init(app)

@app.route('/')
def index():
    images = Image.query.all()
    return render_template('index.html', images=images)

@app.route('/login')
def login():
    return render_template('login.html')  

@app.route('/upload', methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        pic = request.files["pic"]
        
        if not pic:
            return "No picture uploaded", 400
        
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        img = Image(img=pic.read(), filename=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/image/<int:id>')
def get_img(id):
    img = Image.query.get(id)
    if not img:
        return "No image with that id", 404
    
    return Response(img.img, mimetype=img.mimetype)

if __name__ == "__main__":
    app.run(debug=True)
