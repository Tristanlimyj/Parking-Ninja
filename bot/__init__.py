from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
import config

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))

db = SQLAlchemy(app)

from bot.controller import tele_blueprint
app.register_blueprint(tele_blueprint)

