# use flask to make website
from flask import Flask, render_template

# make a new flask app
app = Flask(__name__)

# show home page at "/"
@app.route("/")
def home():
    return render_template("index.html")  # load index page

# show demo page at "/demo"
@app.route("/demo")
def demo():
    return render_template("demo.html")  # load iframe page

# run the app on start
if __name__ == "__main__":
    app.run(debug=True)  # show errors if any
