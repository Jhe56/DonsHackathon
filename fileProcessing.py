#Relearning a lot 
#Disclaimer: I asked chatgpt for an overview of how users would upload image files to display on a webpage
# chatgpt said: 
# 1) front end should be formatted to prompt and receive files, 2) python should be used for back end, 3) CSS or JS for image scaling
# and you should have flask to let you handle html and python

#some credit to Tech with Tim Flask Tutorial PLAYLIST
from flask import Flask, render_template, request

class fileProcessing:

    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("tempForm.html")

    @app.route("/passFile", methods = ["POST","GET"])
    def fileProcessing():
        if request.method == "POST":
            # files given = request.form["fileToUpload"]
            return "FILE"

    if __name__ == "__main__":
        app.run()
