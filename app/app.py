# Import Dependencies 
from flask import Flask, request, render_template, redirect,jsonify
# from flask_assets import Environment, Bundle
from flask_scss import Scss
from datetime import datetime
import os

import json
import pymongo
# import json_utils
from bson.json_util import dumps



# Create an instance of Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

import ETL
@app.route('/Stock_Select', methods=['POST']) 
def Stock_Select(): 
    ETL.Stock_Select(request)
    return render_template('Stocksearch.html')


@app.route('/iframe', methods=['POST']) 
def iframe():
    urls = ['..Project2-Challenge\data\StockETL.csv']
    iframe = (urls)
    return render_template('Stocksearch.html', iframe=iframe) 

@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/Searched_Stock/')
def Searched_Stock():
    return render_template('Stocksearch.html')

@app.route("/sunburst_data.json")
def access_sunburst_data():
    db = client.investopedia
    collection = db.sunburst    
    sunburst_obj =[s for s in collection.find()]
    response= dumps(sunburst_obj)
    print(response)
    return response

 
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


