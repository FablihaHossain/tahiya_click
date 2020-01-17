# Initializing Flask App
from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config
from flask_pymongo import PyMongo
from pymongo import MongoClient

# Creating the Flask App
app = Flask(__name__)
app.config.from_object(Config)

#app.config[Config.MONGODB_URI]
#app.config["MONGO_URI"] = "mongodb://localhost:27017/photo_db"

# Database Connection
db = MongoEngine()
#db = PyMongo(app)
db.init_app(app)