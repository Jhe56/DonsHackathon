from fastapi import FastAPI
from flask import Flask, render_template, request

app = FastAPI()
@app.get("/")


@app.get("/passFile", methods = ["POST","GET"])
async def root():
    return ("Message:", "Hello World")

#so fast api is able to operate as a regular .py file, the main thing is that rather than just that
#it can also return information as json lines, which we can then use to sort of add paths to images into our data banks