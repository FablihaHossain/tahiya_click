import os
from os import path
import pathlib
from application import app, db
from werkzeug import secure_filename
from config import Config
from flask import render_template, session, request, flash, redirect, url_for
from models import Users, Albums
from database import Database

# Login Route
@app.route("/login", methods = ['GET', 'POST'])
def login():
	# Getting the username and password entered
	if request.method == 'POST':
		if request.form['username'] == "" or request.form['password'] == "":
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

				# Getting the corresponding user id
				user_id = Database.get_user_ID(username)
				session['user_id'] = user_id
				return redirect(url_for('albums'))
			else:
				flash("Incorrect login. Please Try Again.")
	return render_template("login.html")

@app.route("/logout")
def logout():
	session.pop('username', None)
	session.pop('user_id', None)
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
				#db = Database.db_connection()
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

	# Current User's ID
	userId = session.get('user_id')

	# Getting all albums in db
	albums_list = Albums.objects.all()
	images = [] # list of all the images all of the albums
	user_albums = [] # list of albums of current user
	other_albums = [] # list of the rest of the albums
	for album in albums_list:
		# Getting all images from each album
		for imgs in album.images:
			images.append(imgs)

		# Getting current logged in user's albums
		if album.owner_id == userId:
			user_albums.append(album)
		else:
			other_albums.append(album)

	# Cover images
	coverImages = []
	for album in albums_list:
		if not album.images == []:
			if album.cover_image == "not_chosen":
				coverImages.append(album.images[0])
			else:
				coverImages.append(album.cover_image)

	return render_template("albumsPage.html", users = users_list, albums = albums_list, user_albums = user_albums, other_albums = other_albums, img = images, coverImages = coverImages, currentUserID = userId)

# Checking if the file uploaded is the appropriate form
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/newAlbum", methods = ['GET', 'POST'])
def newAlbum():
	if not session.get('username'):
		return redirect(url_for('login'))

	# Getting list of current albums in the database
	Albums_list = Albums.objects.all()

	# List to keep track of all albums names currently in db
	currentAlbumNames = []
	for album in Albums_list:
		currentAlbumNames.append(album.name)


	if request.method == 'POST':
		album_name = request.form['name']
		album_description = request.form['description']
		album_images = request.files.getlist("image")
		img = []
		uploaded_files = []
		path_album_name = album_name

		if "" in [album_name, album_description, album_images]:
			flash ("Error! One or more fields is empty! Please fill in ALL the fields")
		elif album_name in currentAlbumNames:
			flash ("Error! Album Name Already Exists. Please Try Again")
		else:
			validFiles = True
			if " " in album_name:
				path_album_name = path_album_name.replace(" ", "_")
			for file in album_images:
				if allowed_file(file.filename):
					newFilename = "/static/images/%s/%s" % (path_album_name, file.filename)
					img.append(newFilename)
					uploaded_files.append(file)
				else:
					flash("Error! Wrong filetype")
					validFiles = False
					break
			if validFiles:
				pathlib.Path(app.config['UPLOAD_FOLDER'], path_album_name).mkdir(exist_ok=True)
				for file in uploaded_files:
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], path_album_name, filename))

				# Getting the user_id of the album creator
				current_user_id = session.get('user_id')
				# Adding new album
				Database.insert_album(album_name, album_description, current_user_id, img)
				flash("Successfully Added Album!")

	return render_template("addAlbum.html")

@app.route("/viewAlbum/<int:albumID>", methods = ['GET', 'POST'])
def viewAlbum(albumID):
	if not session.get('username'):
		return redirect(url_for('login'))

	# Getting all the information for given album id
	currentAlbum = Database.get_album(albumID)

	if currentAlbum == None:
		return redirect((url_for('albums')))
	# Getting all the images in the current album
	currentImages = []
	for img in currentAlbum.images:
		currentImages.append(img)

	# Current User's ID
	userId = session.get('user_id')

	return render_template("viewAlbum.html", album = currentAlbum, img = currentImages, currentUserID = userId)

@app.route("/updateAlbum/<int:albumID>", methods = ['GET', 'POST'])
def updateAlbum(albumID):
	if not session.get('username'):
		return redirect(url_for('login'))

	# Current User's ID
	userId = session.get('user_id')

	# Getting the current album information based on id given
	currentAlbum = Database.get_album(albumID)

	# Only Album Owners can update their own albums 
	if currentAlbum == None or userId != currentAlbum.owner_id:
		return redirect(url_for('albums'))

	# Images list for update form
	images = []

	# Getting all the images in the current album
	currentImages = []
	for img in currentAlbum.images:
		images.append(img) # will be updated in form
		currentImages.append(img) # will not be updated in form

	# Processing the Update Form
	if request.method == 'POST':
		currentAlbum = Database.get_album(albumID) # just in case form refreshes but new changes were made
		# Getting the new changes 
		new_album_name = request.form['name']
		new_album_description = request.form['description']
		new_cover_image = request.form.get('coverImage')
		delete_image_list = request.form.getlist('images')
		new_images_list = request.files.getlist("newImages")

		# List to hold all file names
		uploaded_files = []

		# Updating the album path name in case there are spaces
		path_album_name = new_album_name
		if " " in path_album_name:
			path_album_name = path_album_name.replace(" ", "_")

		# Ensuring no empty fields are submitted
		if "" in [new_album_name, new_album_description]:
			flash("Error! One or more fields was empty...Please remember to fill in ALL the fields")
		else:
			# Deleting Images from Album itself (and from the image folder in application)
			for img in delete_image_list:
				img_albumname = img.split('/')[3] # Getting album pathname
				img_filename = img.split('/')[4] # Getting image filename
				img_pathname = img_albumname + "/" + img_filename # Getting the particular path to be deleted
				os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img_pathname)) # Deleting the image from the directory
				images.remove(img) # Updating the images list for deletion

			# Updating Cover Image (before any potential album name change)
			if new_cover_image is not None:
				print("updating cover image to new chosen image")
				Database.update_db("albums", "album_id", albumID, "cover_image", new_cover_image)

			# If all images were deleted from album, there is no cover image
			if not images:
				print("updating cover image to not chosen")
				Database.update_db("albums", "album_id", albumID, "cover_image", "not_chosen")

			# Getting current file path name based on current Album Name
			currentAlbumName = currentAlbum.name
			if " " in currentAlbumName:
				currentAlbumName = currentAlbumName.replace(" ", "_")

			# If the path alredy exists for the album, it will make the following updates
			if path.exists("application/static/images/%s" % currentAlbumName):
				# Renaming Album File Name in Images Folder
				current_album_path = 'application/static/images/%s' % currentAlbumName
				new_album_path = 'application/static/images/%s' % path_album_name
				os.rename(current_album_path, new_album_path)

				# Updating Routes of Current Images in Album (for new file path)
				for currentImage in images:
					imageName = currentImage.split('/')[4]
					images.remove(currentImage)
					new_pathname_for_current_image = '/static/images/%s/%s' % (path_album_name, imageName)
					images.append(new_pathname_for_current_image)

				# Updating Route of Current Album Cover Image (for new file path)
				currentAlbum = Database.get_album(albumID)
				if currentAlbum.cover_image != "not_chosen":
					currentCoverImage = currentAlbum.cover_image
					print(currentCoverImage)
					coverImageName = currentCoverImage.split('/')[4]
					updatedCoverImagePathName = '/static/images/%s/%s' % (path_album_name, coverImageName)
					print("updating cover image to %s" % updatedCoverImagePathName)
					Database.update_db("albums", "album_id", albumID, "cover_image", updatedCoverImagePathName) 

			# Updating album name in db
			Database.update_db("albums", "album_id", albumID, "name", new_album_name)

			# Updating album description in db
			Database.update_db("albums", "album_id", albumID, "description", new_album_description)

			# Boolean to keep track of validity of newly updateds files
			validFiles = True

			# List of files to inform user that name of file already exists in the album
			duplicateFilePaths = []

			# Parsing through all files that was uploaded
			for file in new_images_list:
				name_of_file = file.filename
				# Checking file extension 
				if allowed_file(name_of_file):
					# If there are spaces in the file name, replaces them with underscore
					if " " in name_of_file:
						name_of_file = name_of_file.replace(" ", "_")

					# Pathname and Filename for the uploaded image
					pathname = "application/static/images/%s/%s" % (path_album_name, name_of_file)
					newFilename = "/static/images/%s/%s" % (path_album_name, name_of_file)

					# If path name doesn't exist, it appends the new filename to image list. It goes to the duplicate list otherwise
					if os.path.exists(pathname):
						duplicateFilePaths.append(pathname)
					elif newFilename not in images:
						images.append(newFilename)
						uploaded_files.append(file)
				else:
					# Disregards form if wrong file extension was uploaded
					flash("Error! Wrong filetype")
					validFiles = False
					break

			# If uploaded file name exists already, prompts user to rename and re-upload image files
			if duplicateFilePaths:
				validFiles = False
				flash("Error... Following Filename Already Exists in Album:")
				for file in duplicateFilePaths:
					flash(file.split('/')[4])

			# If all the files uploaded are valid, then continue to upload
			if validFiles:
				for file in uploaded_files:
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], path_album_name, filename))

				# Updating album images field in the db
				Database.update_db("albums", "album_id", albumID, "images", images)

				# Redirecting to album page
				return redirect(url_for('albums'))

	return render_template("updateAlbum.html", album = currentAlbum, img = currentImages)

# Credit to https://gist.github.com/liulixiang1988/cc3093b2d8cced6dcf38
# Credit to https://stackoverflow.com/questions/31859903/get-the-value-of-a-checkbox-in-flask
# Credit to https://stackoverflow.com/questions/52814669/flask-create-and-upload-files-into-folders-dynamically
# Credit to https://www.guru99.com/python-rename-file.html