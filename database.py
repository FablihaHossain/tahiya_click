from application import db
from models import Users, Albums

class Database():
	# insert_user: This function will insert data to the Users table
	def insert_user(fname, lname, email, user, pw, role):
		# Getting List of current users in the database
		Users_list = Users.objects.all()

		# Getting the last user_id in the table
		lastUserID = Users.objects.count()

		# Generating a new ID for the new user
		newId = lastUserID + 1

		# Creating new user with given data
		newUser = Users(user_id = newId, firstname = fname, lastname = lname, email = email, username = user, password = pw, role = role)

		# Checks to see if new user currently exists in the database with given email address
		exists = False
		for user in Users_list:
			if user.email == newUser.email:  
				exists = True

		# If user doesn't exist in the database, it is finally inserted into the users table
		if not exists:
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
		newAlbum = Albums(album_id = nextID, name = name, description = description, owner_id = owner_id, images = img)
		
		# Checking to see if album already exists in the database with given name and owner id
		exists = False
		for album in Albums_list:
			if album.name == name and album.owner_id == owner_id:
				exists = True

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
			if(columnName == "title"):
				intendedAlbum.update(set__title = newValue)
			elif(columnName == "description"):
				intendedAlbum.update(set__description = newValue)
			elif(columnName == "images"):
				intendedAlbum.update(set__images = newValue)
			else:
				return "Error... Column Name not found"
		elif tableName == "users" and pkColumn == "user_id":
			# Getting the row
			intendedUser = Users.objects(user_id = pk)
			# Updaing the row
			intendedUser.update(columnName = newValue)
		else:
			return "Error... Wrong table given"

	# Delete_db: Delete a particular row from database
	#def delete_db()
