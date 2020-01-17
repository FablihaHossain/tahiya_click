from application import app, db
from config import Config
from flask import render_template, session
from models import Users, Albums
from database import Database

# app = Flask(__name__)
# app.config.from_object(Config)

# db = MongoEngine()
# db.init_app(app)

# Defining Basic route
@app.route("/")

def index():
	# Testing update function for user
	Database.update_db("users", "user_id", 3, "lastname", "Sommerville")

	# Getting all users in db
	users_list = Users.objects.all()

	return render_template("index.html", users = users_list)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/albums")
def albums():
	# img = ["/static/images/IMG_4720.jpg", "/static/images/IMG_4721.jpg"]
	# Albums(album_id = 1, name = "Nature Pictures", description = "Inspirational Pictures of Natural Environment", images = img).save()

	# currentAlbum = Albums.objects(album_id =1)
	# currentAlbum.update(description = "Enjoying The Great Outdoors")

	# Removing from table
	# removeUser = Users.objects(user_id = 2)
	# removeUser.delete()


	# Testing insert users function
	Database.insert_user("John", "Smith", "jsmith@gmail.com", "jsmith", "mystery", "general user")

	# Getting all users in db
	users_list = Users.objects.all()

	# Testing insert albums function
	pics = ["static/images/IMG_1234.jpg", "static/images/IMG_3835.JPG"]
	Database.insert_album("Chicago Adventure", "Some photos I took in Chicago during the Summer of 2019", 1, pics)


	# Testing Update function in db
	#Database.update_db("albums", "album_id", 2, "description", "Chicago Weekend 2019")
	#intendedAlbum = Albums.objects(album_id = 2)
	#intendedAlbum.update(set__description = "Weekend in Chicago")
	#intendedAlbum.description = "Nature Pictures"
	#intendedAlbum.save()

	# Getting all albums in db
	albums_list = Albums.objects.all()
	images = []
	for album in albums_list:
		for imgs in album.images:
			images.append(imgs)

	return render_template("albumsPage.html", users = users_list, albums = albums_list, img = images)
