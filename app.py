# Initializing Flask App
from flask import Flask
from flask import render_template

app = Flask(__name__)

# Defining Basic route
@app.route("/")
def index():
	return render_template("index.html")

# Running the flask app
if __name__ == "__main__":
	app.run(debug = True)
