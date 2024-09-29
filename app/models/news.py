from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from .base import BASE
from flask_login import UserMixin
import os
from dotenv import load_dotenv

class News(BASE):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    news = Column(String(150), nullable=False)
    image = Column(String(150), nullable=False)