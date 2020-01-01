# Initializing Flask App
# from flask import Flask
# from flask_mongoengine import MongoEngine
# from config import Config
from application import app, db
from flask import render_template
from models import Users, Albums, AlbumImage

# app = Flask(__name__)
# app.config.from_object(Config)

# db = MongoEngine()
# db.init_app(app)

# Defining Basic route
@app.route("/")
def index():
	# Getting all users in db
	users_list = Users.objects.all()

	# image1 = AlbumImage()
	# imageFile1 = open('application/static/images/IMG_4721.jpg', 'rb')
	# image1.image.put(imageFile1, content_type = 'image/png')

	# image2 = AlbumImage()
	# imageFile2 = open('application/static/images/IMG_4720.JPG', 'rb')
	# image2.image.put(imageFile2, content_type = 'image/png')

	# newAlbum = Albums()
	# newAlbum.album_id = 1
	# newAlbum.name = "Nature Photos"
	# newAlbum.description = "Pictures of Nature"
	# newAlbum.images.append(image1)
	# newAlbum.images.append(image2)
	# newAlbum.save()

	albums_list = Albums.objects.all()
	images = []
	for album in albums_list:
		for img in album.images:
			images.append(img)

	return render_template("index.html", users = users_list, albums = albums_list, img = images)
