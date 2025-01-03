from sqlalchemy import create_engine, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from .base import BASE
from flask_login import UserMixin
import os
from dotenv import load_dotenv

class User(BASE, UserMixin):
    __tablename__ = 'registrations'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    admin = Column(Boolean, default=False, nullable=False)