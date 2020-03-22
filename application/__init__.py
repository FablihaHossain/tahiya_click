# Initializing Flask App
from flask import Flask
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from config import Config

# Creating the Flask App
app = Flask(__name__)

# Configuring it with secret key
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# client = MongoClient("mongodb://127.0.0.1:54758")
# db = client.photo_db


#Database Connection
db = MongoEngine()
db.init_app(app)
app.config['MONGODB_SETTINGS'] = {'db': 'photo_db', 'username': Config.user, 'password': Config.pwd}

# Initial connection for the application launch
#db = db_connection()

# File location for all the images
UPLOAD_FOLDER = 'application/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Credit to https://flask.palletsprojects.com/en/1.1.x/quickstart/
# Credit to https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/