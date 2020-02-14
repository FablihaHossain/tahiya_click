from application import app, db
from config import Config
from flask import render_template, session, request, flash, redirect, url_for
from models import Users, Albums
from database import Database

# app = Flask(__name__)
# app.config.from_object(Config)

# db = MongoEngine()
# db.init_app(app)

# Login Route
@app.route("/login", methods = ['GET', 'POST'])
def login():
	# Getting the username and password entered
	if request.method == 'POST':
		if request.form['username'] is "" or request.form['password'] is "":
			flash("Error! Fields cannot be empty!")
		else:
			# Getting the username and password entered
			username = request.form['username']
			password = request.form['password']

			# Checking if correct credentials were given
			valid_user = Database.check_user(username, password)

			# Creating a session in order to continue with the application
			if valid_user is True:
				session['username'] = username
				return redirect(url_for('albums'))
			else:
				flash("Incorrect login. Please Try Again.")
	return render_template("login.html")

@app.route("/logout")
def logout():
	session.pop('username', None)
	flash("You have logged out successfully")
	return redirect(url_for('login'))

@app.route("/register", methods = ['GET', 'POST'])
def register():
	if session.get('username'):
		return redirect(url_for('blogs'))

	if request.method == 'POST':
		# Getting all the information
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']

		# Ensuring that all fields are filled in
		if "" in [firstname, lastname, email, username, password]:
			flash("Error! One or more fields is empty! Please fill in ALL the fields")
		else:
			# Checking if email address already exists
			email_exist = Database.check_duplicate_user("email", email)

			# Checking if username already exists
			username_exist = Database.check_duplicate_user("username", username)

			# If email or username is already in db, a warning message is given
			if email_exist is True:
				flash("Error! Email Address already taken! Please Try Another One")
			elif username_exist is True:
				flash("Error! Username already exists. Please Try Another One")
			else:
				# Adding the user to database
				Database.insert_user(firstname, lastname, email, username, password, "general user")
				flash("Congradulations! You've been registered!")
				return redirect(url_for('albums'))
	return render_template("register.html")

# Defining Basic route
@app.route("/")
def index():
	# Testing update function for user
	Database.update_db("users", "user_id", 3, "username", "jsommerville")

	# Testing deletion
	Database.insert_user("Jake", "Murry", "jmurry@gmail.com", "jmurry", "sfhsffs", "general user")

	#Database.delete_db("users", "user_id", 4)
	# Getting all users in db
	users_list = Users.objects.all()

	return render_template("index.html", users = users_list)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/albums")
def albums():
	if not session.get('username'):
		return redirect(url_for('login'))
	# img = ["/static/images/IMG_4720.jpg", "/static/images/IMG_4721.jpg"]
	# Albums(album_id = 1, name = "Nature Pictures", description = "Inspirational Pictures of Natural Environment", images = img).save()

	currentAlbum = Albums.objects(album_id =1)
	currentAlbum.update(owner_id = "2")

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

	# Cover images
	coverImages = []
	for album in albums_list:
		coverImages.append(album.images[0]) 

	return render_template("albumsPage.html", users = users_list, albums = albums_list, img = images, coverImages = coverImages)
