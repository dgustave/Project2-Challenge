# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from flask_assets import Environment, Bundle
from flask_scss import Scss
import os



# Create an instance of Flask app
app = Flask(__name__)
assets_folder = os.path.join(app.root_path, 'assets')

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
