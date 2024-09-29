from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = create_engine(os.getenv("DATABASE_URL"))
SESSION = sessionmaker(DATABASE)
session = SESSION()

BASE = declarative_base()

def create_db():
    BASE.metadata.create_all(DATABASE)