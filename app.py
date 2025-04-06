from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from database import Sessionlocal, engine
from models import Image, Base
import os
import imghdr
import uuid
from flask import request, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
Scss(app)


app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.config["UPLOAD_PATH"] = "uploads"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize DB (create tables)
Base.metadata.create_all(bind=engine)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')  

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


class Images(Resource):
    def post(self):
        info = request.form.get("info")
        image_name = request.form.get("image_name")
        image = request.files.get("image")

        # check if filepath already exists. append random string if it does
        if secure_filename(image.filename) in [
            img.file_path for img in Image.query.all()
        ]:
            unique_str = str(uuid.uuid4())[:8]
            image.filename = f"{unique_str}_{image.filename}"


        #  handling file uploads
        filename = secure_filename(image.filename)
        if filename:
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config[
                "UPLOAD_EXTENSIONS"
            ] or file_ext != validate_image(image.stream):
                return {"error": "File type not supported"}, 400

            image.save(os.path.join(app.config["UPLOAD_PATH"], filename))

            img = Image(name=image_name, file_path=filename)

            db.session.add(img)
            db.session.commit()
            
    class Images(Resource):
        def get(self, id):
            img = Image.query.filter(Image.id == id).first()
            path = img.file_path
            return send_from_directory(app.config["UPLOAD_PATH"], path)

if __name__ == "__main__":
    app.run(debug=True)
