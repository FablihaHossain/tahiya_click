# Initializing Flask App
from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config

# Creating the Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Database Connection
db = MongoEngine()
db.init_app(app)