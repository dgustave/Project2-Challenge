# Import Dependencies 
from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
from flask_assets import Environment, Bundle
from flask_scss import Scss
from datetime import datetime
import os



# Create an instance of Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/Searched_Stock/')
def Searched_Stock():
    return render_template('Stocksearch.html')

import ETL
@app.route('/Stock_Select', methods=['POST']) 
def Stock_Select(): 
    ETL.Stock_Select()
    return render_template('Stocksearch.html') 

  


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


