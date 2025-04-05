#Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

#App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

#Data Class ~ Row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    complete = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"Task {self.id} - {self.content}"

@app.route('/', methods = ["GET", "POST"])
def index():
    #Add Task
    if request.method == "POST":
        current_task = request.form.get("content")
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return(f"Error: {e}")     
    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created.desc()).all()
        return render_template('index.html', tasks=tasks)
    
    
    
    
    #return home page
    return render_template('index.html')



@app.route('/login')
def login():
    return render_template('login.html')    

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)