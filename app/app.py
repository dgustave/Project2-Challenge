# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_assets import Environment, Bundle
from flask_scss import Scss
from pymongo import MongoClient
from Missions_to_Mars import scrape_mars
import os



# Create an instance of Flask app
app = Flask(__name__)

# Enable js features and extend to my templates: 
assets = Environment(app)

# Route jinjas templating to correct locations:
Scss(app, static_dir='static', asset_dir='assets')

# Enable bootsrap features and extend to my templates: 
bootstrap = Bootstrap(app)


# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
app.config['MONGO_DBNAME'] = 'mars_app'
mongo = PyMongo(app)
print ("MongoDB Database:", mongo.db)


# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 
    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("base.html", mars_dict=mars_dict)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 
    # Run scrapped functions
    mars_dict = mongo.db.mars_dict
    scrape_all = scrape_mars.run()
    # title = mongo.db.mars_dict.find_one_or_404({'title': title})
    # teaser_html = mongo.db.mars_dict.find_one_or_404({'summary': teaser_html})
    # featured_image_link = mongo.db.mars_dict.find_one_or_404({'featured_image': featured_image_link})
    # fact_html = mongo.db.mars_dict.find_one_or_404({'fact_table': fact_html})

    mars_dict.update({}, scrape_all, upsert = True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
