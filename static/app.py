from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "It works!"

if __name__ == '__main__':
    app.run()