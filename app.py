# Initializing Flask App
# from flask import Flask
# from flask_mongoengine import MongoEngine
# from config import Config
from application import app, db
from flask import render_template
from models import Users, Albums

# app = Flask(__name__)
# app.config.from_object(Config)

# db = MongoEngine()
# db.init_app(app)

# Defining Basic route
@app.route("/")
def index():
	# Getting all users in db
	users_list = Users.objects.all()

	return render_template("index.html", users = users_list)
