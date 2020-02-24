# Initializing Flask App
from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config

# Creating the Flask App
app = Flask(__name__)

# Configuring it with secret key
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Database Connection
db = MongoEngine()
db.init_app(app)

# File location for all the images
UPLOAD_FOLDER = 'application/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Credit to https://flask.palletsprojects.com/en/1.1.x/quickstart/
# Credit to https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/