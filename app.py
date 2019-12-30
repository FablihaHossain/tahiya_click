# Initializing Flask App
from flask import Flask
from flask import render_template
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

class Users(db.Document):
	user_id = db.IntField(unique = True)
	firstname = db.StringField(max_length = 50)
	lastname = db.StringField(max_length = 50)
	username = db.StringField(max_length = 50)
	password = db.StringField(max_length = 50)

# Defining Basic route
@app.route("/")
def index():
	# Getting all users in db
	users_list = Users.objects.all()
	return render_template("index.html", users = users_list)

# Running the flask app
if __name__ == "__main__":
	app.run(debug = True)
