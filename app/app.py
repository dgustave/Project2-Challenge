# Import Dependencies 
from flask import Flask, request, render_template, redirect, jsonify, url_for 
from flask_pymongo import PyMongo
from flask_assets import Environment, Bundle
from flask_scss import Scss
import pymongo
from datetime import datetime
from pymongo import MongoClient
from flask import jsonify, json, request
from bson.json_util import dumps
from bson.objectid import ObjectId
# import datetime as dt
from dateutil.parser import parse
import sys
import numpy as np
import os
import csv

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)



# Create an instance of Flask app
app = Flask(__name__)

@app.route('/')
def index():
    db = client['WallStreet']
    sp_collection = db["SP500_Change"]
    table = sp_collection.find_one()
    print(table)
    return render_template('index.html', table=table)
@app.route('/tables') 
def stable():
    db = client['WallStreet']
    hp_collection = db["HP"]
    hdata = hp_collection.find_one()
    print(hdata)
    return render_template("tables.html", hdata=hdata)

import ETL
@app.route('/Stock_Select', methods=['POST']) 
def Stock_Select(): 
    ETL.Stock_Select(request)
    return render_template('Stocksearch.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/StockETL/')
def StockETL():
    return render_template('StockETL.html')

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
    

    response = dumps({"response": sunburst_obj})
    return response

@app.route('/User-Profile/')
def user():

    return render_template('user.html')

@app.route('/candle') 
def candle():
    with open('../data/processed/NCR.csv') as csv_file:
            
        data = csv.reader(csv_file, delimiter=',')
        first_line = True
        sdata = []
        for row in data:
            if not first_line:
                sdata.append({"TIMESTAMP": row[0], "OPEN": row[1], "HIGH": row[2], "LOW ": row[3], "CLOSE": row[4], "TURNOVER": row[5], "VOLATILITY": row[6]})
            else:
                first_line = False
        return render_template("icons.html", sdata=sdata)

@app.route('/NCR.json') 
def NRC_Select(): 
    db = client['yfinancing']
    yf_collection = db["NCR"]
    x_list = list(yf_collection.find())

    ncr_data= x_list[0]
    # d = datetime.datetime.strptime(x['TIMESTAMP'],'%Y-%m-%d')
    # stock_data = [x for x in  yf_collection.find()]
    stock_data = []
    # newtime = [] 
    # .strftime('%Y-%m-%d')
    for x, date in enumerate(ncr_data['TIMESTAMP']):
        timestamp = date.strftime('%Y-%m-%d')
        # listToStr = map(str, timestamp)
        # time=[i for i in listToStr if not i in ["/"]]
        # # dates = time.split()

        # print(x['TIMESTAMP'])
        # unixtime = x['TIMESTAMP'][:-3]
    #     for j in unixtime:
    #         ts = int(j)
    #         dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    #     # print(x.keys())
        # stock_data.append({'STOCK': [x['CLOSE'], x['HIGH'], x['LOW '], x['OPEN'],  timestamp , x['TURNOVER'], x['VOLATILITY']]})
# for i, date in enumerate(ncr_data['TIMESTAMP']):
#     mydict = {'CLOSE': ncr_data['CLOSE'][e], 'HIGH': ncr_data['HIGH'][e] , 'LOW': ncr_data['LOW '][e], 'OPEN': ncr_data['OPEN'][e] , 'TIMESTAMP': date, 'TURNOVER': ncr_data['TURNOVER'][e], 'VOLATILITY': ncr_data['VOLATILITY'][e]}
 
        stock_dict = {'TIMESTAMP': timestamp , 'OPEN': ncr_data['OPEN'][x], 'HIGH': ncr_data['HIGH'][x], 'LOW': ncr_data['LOW '][x], 'CLOSE': ncr_data['CLOSE'][x], 'TURNOVER': ncr_data['TURNOVER'][x], 'VOLATILITY': ncr_data['VOLATILITY'][x]}
        stock_data.append(stock_dict)
    # # print(type(timestamp[0]))
    return dumps({"NCR": stock_data})


 
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


