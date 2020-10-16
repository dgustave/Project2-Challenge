# Import Dependencies 
from flask import Flask, request, render_template, redirect,jsonify,url_for
from flask_assets import Environment, Bundle
from flask_scss import Scss
from datetime import datetime
import os

import json
import pymongo
# import json_utils
from bson.json_util import dumps
import sys
import numpy as np

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)



# Create an instance of Flask app
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    db = client.investopedia
    collection = db.sunburst
    sunburst_obj = collection.find() 
    response= dumps(sunburst_obj)
    # print(response)
    data = {'chart_data': response}
    return render_template('index.html', sunburst=data)
    # return render_template('index.html',response=response)

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

@app.route("/tester.json")
def tester():
    db = client.investopedia
    collection = db.sunburst 
    sunburst_obj =[] 
    for s in collection.find():
        parents=[]
        for x in s['parents']:
            if isinstance(x,float):
                a=""
            else:
                a=x
            parents.append(a)
        s['parents']=parents
        sunburst_obj.append(s)
    
        

    
    # response= dumps(sunburst_obj)

    response = dumps({"response": sunburst_obj})
    # print(response)
    return response



 
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


