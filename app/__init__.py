from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from app.models.base import create_db
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app=app)

create_db()
from . import routes