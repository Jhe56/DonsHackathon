from fastapi import FastAPI
from flask import Flask, render_template, request

app = FastAPI()

@app.get("/")
async def root():
    return ("Message:", "Hello World")