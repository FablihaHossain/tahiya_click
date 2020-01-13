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

# cursor = mongo.db.measurements.find().sort([('timestamp', -1)]).limit(1)

		
