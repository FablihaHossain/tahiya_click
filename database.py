from application import app, db, hashing
from flask_mongoengine import MongoEngine
from models import Users, Albums
from config import Config

class Database():
	# Function that checks for duplicates before inserting or updating certain types of data
	# returns either true if the value of the column name exists at given table, false otherwise
	def check_duplicate_user(columnName, value):
		# Getting List of current users in the database
		Users_list = Users.objects.all()

		# Initial value of false
		exists = False
		# Parsing through users table
		for user in Users_list:
			# Emails and Usernames cannot be the same for two users
			if(columnName == "email" and user.email == value):
				exists = True
			elif(columnName == "username" and user.username == value):
				exists = True
			else:
				exists = False
		return exists

	def check_duplicate_album(nameValue, owner_idValue):
		# Getting list of current albums in the database
		Albums_list = Albums.objects.all()

		# Parsing through the albums table
		for album in Albums_list:
			# Checking to see if Album owner already has an album with same name
			if(album.name == nameValue and album.owner_id == owner_idValue):
				exists = True
			else:
				exists = False
		return exists 

	# insert_user: This function will insert data to the Users table
	def insert_user(fname, lname, email, user, pw, role):
		# Getting List of current users in the database
		Users_list = Users.objects.all()

		# Getting the last user_id in the table
		lastUserID = Users.objects.count()

		# Generating a new ID for the new user
		newId = lastUserID + 1

		# Hashing the password
		password_hash = Database.hash_password(pw)

		# Creating new user with given data
		newUser = Users(user_id = newId, firstname = fname, lastname = lname, email = email, username = user, password = password_hash, role = role)

		# Checks to see if new user currently exists in the database with given email address and username
		email_exists = Database.check_duplicate_user("email", email)
		username_exists = Database.check_duplicate_user("username", user)

		# If user doesn't exist in the database, it is finally inserted into the users table
		if not email_exists and not username_exists:
			newUser.save()

	# insert_album: This function creates a new album in the database
	def insert_album(name, description, owner_id, img):
		# Getting list of current albums in the database
		Albums_list = Albums.objects.all()

		# Getting the last album_id in the table
		lastAlbumID = Albums.objects.count()

		# Generating new ID for new album
		nextID = lastAlbumID + 1

		# Creating new album with given data
		newAlbum = Albums(album_id = nextID, name = name, description = description, owner_id = owner_id, images = img, cover_image = "not_chosen")
		
		# Checking to see if album already exists in the database with given name and owner id
		exists = Database.check_duplicate_album(name, owner_id)

		# Adding new album to the database if it doesn't already exist
		if not exists:
			newAlbum.save()

	# Update_db: Update a row in the database
	# Using the primary key column and value to get the particular row
	def update_db(tableName, pkColumn, pk, columnName, newValue):
		if tableName == "albums" and pkColumn == "album_id":
			# Getting the row
			intendedAlbum = Albums.objects(album_id = pk)
			# Updating the row
			if(columnName == "name"):
				intendedAlbum.update(set__name = newValue)
			elif(columnName == "description"):
				intendedAlbum.update(set__description = newValue)
			elif(columnName == "images"):
				intendedAlbum.update(set__images = newValue)
			elif(columnName == "cover_image"):
				intendedAlbum.update(set__cover_image = newValue)
			else:
				print("Error... Column Name not found")
		elif tableName == "users" and pkColumn == "user_id":
			# Getting the row
			intendedUser = Users.objects(user_id = pk)
			# Updaing the row
			if(columnName == "firstname"):
				intendedUser.update(set__firstname = newValue)
			elif(columnName == "lastname"):
				intendedUser.update(set__lastname = newValue)
			elif(columnName == "email"):
				# Checks if email already exists in database
				exists = Database.check_duplicate_user("email", newValue)
				if not exists:
					intendedUser.update(set__email = newValue)
			elif(columnName == "username"):
				# Checks if username already exists in database
				exists = Database.check_duplicate_user("username", newValue)
				if not exists:
					intendedUser.update(set__username = newValue)
			elif(columnName == "password"):
				intendedUser.update(set__password = newValue)
			else:
				print("Error... Column Name not found")
		else:
			print("Error... Wrong table or Primary Key given")
# Credit to http://docs.mongoengine.org/tutorial.html

	# Delete_db: Delete a particular row from database
	def delete_db(tableName, pkColumn, pk): 
		if(tableName == "users" and pkColumn == "user_id"):
			removeUser = Users.objects(user_id = pk)
			removeUser.delete()
		elif(tableName == "albums" and pkColumn == "album_id"):
			removeAlbum = Albums.objects(album_id = pk)
			removeAlbum.delete()
		else:
			return "Error... Wrong Table Given"

	# Check Log In Function to validate the user 
	# Returns True if the username and password correspond, false otherwise
	def validate_login(username, password):
		# Getting List of current users in the database
		Users_list = Users.objects.all()
		# initially invalid log in
		valid = False

		# Going through all users in the database
		for user in Users_list:
			# Validating username and password (using hashing function)
			if user.username == username and Database.validate_password_hash(password, user.password):
				valid = True

		return valid

	# Function to get the album data given an album ID
	def get_album(albumID):
		# Getting list of current albums in the database
		Albums_list = Albums.objects.all()

		for album in Albums_list:
			if album.album_id == albumID:
				return album

	# Function to get the user_id of the given username
	def get_user_ID(username):
		# Getting List of current users in the database
		Users_list = Users.objects.all()

		for user in Users_list:
			if user.username == username:
				return user.user_id

	# Function to Hash password (using flask-hashing)
	def hash_password(plaintext, salt='fab'):
		try:
			# Creating the password hash
			password_hash = hashing.hash_value(plaintext)

			# Return the hashed password
			return password_hash
		except Exception as error:
			print("Error... %s" % error)

	# Function to check password hashes to check if equal or not
	def validate_password_hash(password, password_hash, salt='fab'):
		try:
			# Using hashing function to check values
			validate = hashing.check_value(password_hash, password)

			# Returning the value
			return validate
		except Exception as error:
			print("Error... %s" % error)


