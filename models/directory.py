from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from wtforms import EmailField
from .base import BASE
from flask_login import UserMixin
import os
from dotenv import load_dotenv

class Directory(BASE):
    __tablename__ = 'directory'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    file = Column(String(100), nullable=False)