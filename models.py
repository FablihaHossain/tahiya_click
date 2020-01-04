# Credit to https://tutorials.technology/tutorials/Mongoengine-How-to-use-filefield-for-storing-images-and-files.html
import flask
from application import db
from mongoengine import Document
from mongoengine import ListField, FileField, EmbeddedDocument, EmbeddedDocumentField, StringField

class Users(db.Document):
	user_id = db.IntField(unique = True)
	firstname = db.StringField(max_length = 50)
	lastname = db.StringField(max_length = 50)
	username = db.StringField(max_length = 50)
	password = db.StringField(max_length = 50)

class Albums(db.Document):
	album_id = db.IntField(unique = True)
	name = db.StringField(max_length = 50)
	description = db.StringField(max_length = 100)
	# Array of names of Image Files
	images = ListField(StringField(max_length = 200))
	