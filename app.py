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
	#img = ["/static/images/IMG_4720.jpg", "/static/images/IMG_4721.jpg"]
	#Albums(album_id = 1, name = "Nature Pictures", description = "Inspirational Pictures of Natural Environment", images = img).save()

	# Getting all users in db
	users_list = Users.objects.all()

	# Getting all albums in db
	albums_list = Albums.objects.all()
	images = []
	for album in albums_list:
		for imgs in album.images:
			images.append(imgs)

	return render_template("index.html", users = users_list, albums = albums_list, img = images)
