from application import app, db
from config import Config
from flask import render_template, session, request, flash, redirect, url_for
from models import Users, Albums
from database import Database

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
			valid_user = Database.validate_login(username, password)

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
		return redirect(url_for('albums'))

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

	# Getting all users in db
	users_list = Users.objects.all()

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

@app.route("/newAlbum", methods = ['GET', 'POST'])
def newAlbum():
	if not session.get('username'):
		return redirect(url_for('login'))

	if request.method == 'POST':
		album_name = request.form['name']
		album_description = request.form['description']
		album_images = request.form.getlist("imagefiles[]")

		if "" in [album_name, album_description]:
			flash ("Error! One or more fields is empty! Please fill in ALL the fields")
		else:
			flash (album_images)
	return render_template("addAlbum.html")

@app.route("/viewAlbum/<int:albumID>", methods = ['GET', 'POST'])
def viewAlbum(albumID):
	if not session.get('username'):
		return redirect(url_for('login'))

	# Getting all the information for given album id
	currentAlbum = Database.get_album(albumID)

	return render_template("viewAlbum.html", album = currentAlbum)

