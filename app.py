from flask import Flask, render_template  # Import Flask for web app

app = Flask(__name__)  # Create Flask app instance

@app.route("/")  # Home page route defined

def home():  # Function serves home page content
    return render_template("index.html")  # Render index HTML page

@app.route("/demo")  # Demo page route defined

def demo():  # Function serves demo page content
    return render_template("demo.html")  # Render demo HTML page

@app.route("/login")  # Login page route defined

def login():  # Function serves login page content
    return render_template("login.html")  # Render login HTML page

@app.route("/signup")  # Signup page route defined

def signup():  # Function serves signup page content
    return render_template("signup.html")  # Render signup HTML page

@app.route("/upload_books")  # Upload books route defined

def upload_books():  # Function serves upload books page
    return render_template("upload_books.html")  # Render upload books HTML

if __name__ == "__main__":  # Run app from main script
    app.run(debug=True)  # Run Flask app debugging enabled
