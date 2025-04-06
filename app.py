from database import db_init, db
from flask import Flask, render_template, redirect, url_for, request, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_scss import Scss
from sqlalchemy.orm import Session
# from database import Sessionlocal, engine
from models import Image
from flask import request, session, send_from_directory
from werkzeug.utils import secure_filename
from models import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    images = Image.query.all()
    return render_template('index.html', images=images)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        pic = request.files.get("pic")

        if not pic:
            flash("No picture uploaded!")
            return redirect(request.url)

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        if not filename or not mimetype:
            flash("Invalid upload.")
            return redirect(request.url)

        img = Image(img=pic.read(), filename=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        flash("Upload successful!")

        return redirect(url_for('index'))

    return render_template('upload.html')



@app.route('/image/<int:id>')
def get_img(id):
    img = Image.query.get(id)
    if not img:
        return "No image with that id", 404

    return Response(img.img, mimetype=img.mimetype)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('marketplace'))
        flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post_book', methods=['GET', 'POST'])
@login_required
def post_book():
    if request.method == 'POST':
        title = request.form['title']
        course = request.form['course']
        price = float(request.form['price'])
        contact_info = request.form['contact_info']

        new_book = Book(title=title, course=course, price=price,
                        contact_info=contact_info, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book posted successfully!')
        return redirect(url_for('marketplace'))

    return render_template('post_book.html')

@app.route('/marketplace')
@login_required
def marketplace():
    books = Book.query.all()
    return render_template('marketplace.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
