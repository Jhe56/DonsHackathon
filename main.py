from fastapi import FastApi
from flask import Flask, render_template, request

app = FastApi()

@app.get("/")
async def root():
    return ("Message:", "Hello World")