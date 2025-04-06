from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
# from database import Base
from database import db


class Image(db.Model):
    __tablename__ = "images"

    # layouts
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
