from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    
    #Image data 
    image_id = Column(String, index=True) #image id
    image_url= Column(String, index=True) #image url