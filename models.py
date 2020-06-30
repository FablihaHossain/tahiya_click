import flask
from application import db
from mongoengine import Document
from mongoengine import ListField, StringField, IntField

# Users Table
class Users(Document):
	user_id = IntField(unique = True)
	firstname = StringField(max_length = 50)
	lastname = StringField(max_length = 50)
	email = StringField(max_length = 100)
	username = StringField(max_length = 50)
	password = StringField(max_length = 100)
	role = StringField(max_length = 20)

# Albums Table
class Albums(Document):
	album_id = IntField(unique = True)
	name = StringField(max_length = 50)
	description = StringField(max_length = 100)
	owner_id = IntField() # User ID of the one that created the album
	images = ListField(StringField(max_length = 200)) # Array of names of Image Files
	cover_image = StringField(max_length = 2000) # Cover Image defaults to first image in album, unless specified otherwise


	