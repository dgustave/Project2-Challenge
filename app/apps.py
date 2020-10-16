# Import Dependencies 
from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
from flask_assets import Environment, Bundle
from flask_scss import Scss
import pymongo
from pymongo import MongoClient
from flask import jsonify, json, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime as dt
from dateutil.parser import parse
import os

client =  MongoClient("mongodb://localhost:27017")



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

@app.route('/icons.html') 
def candle():
    return render_template('icons.html')

@app.route('/NCR.json') 
def NRC_Select(): 
    db = client['yfinancing']
    yf_collection = db["NCR"]
    # d = datetime.datetime.strptime(x['TIMESTAMP'],'%Y-%m-%d')
    # stock_data = [x for x in  yf_collection.find()]
    stock_data = []
    # newtime = [] 
    # .strftime('%Y-%m-%d')
    for x in yf_collection.find():
        timestamp = [d.strftime('%Y-%m-%d')for d in x['TIMESTAMP']]
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
        stock_data.append({'CLOSE': x['CLOSE'], 'HIGH': x['HIGH'], 'LOW': x['LOW '], 'OPEN': x['OPEN'], 'TIMESTAMP':  timestamp , 'TURNOVER': x['TURNOVER'], 'VOLATILITY': x['VOLATILITY']})
    
    # # print(type(timestamp[0]))
    return dumps(stock_data)

# @app.route('/BIO.json', methods=['POST']) 
# def Stock_Select(): 
#     ETL.Stock_Select()
#     return render_template('Stocksearch.html')   

# @app.route('/CVS.json', methods=['POST']) 
# def Stock_Select(): 
#     ETL.Stock_Select()
#     return render_template('Stocksearch.html')   

# ENR 
# LVGO 
# NCR 
# NEM 
# PODD 
# PWR 
# SMG 
# VRT 
# XRX 




if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


