import flask
from application import db
from mongoengine import Document
from mongoengine import ListField, StringField, IntField

# Users Table
class Users(db.Document):
	user_id = db.IntField(unique = True)
	firstname = db.StringField(max_length = 50)
	lastname = db.StringField(max_length = 50)
	email = db.StringField(max_length = 100)
	username = db.StringField(max_length = 50)
	password = db.StringField(max_length = 100)
	role = db.StringField(max_length = 20)

# Albums Table
class Albums(db.Document):
	album_id = db.IntField(unique = True)
	name = db.StringField(max_length = 50)
	description = db.StringField(max_length = 100)
	owner_id = db.IntField() # User ID of the one that created the album
	images = ListField(StringField(max_length = 200)) # Array of names of Image Files


	