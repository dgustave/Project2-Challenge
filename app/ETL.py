import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from flask import request
from flask import Flask 
from flask import request 
import datetime
from pymongo import MongoClient
import numpy as np
import json
import pandas_profiling
from pandas_profiling import ProfileReport


app = Flask(__name__)

@app.route('/Stock_Select', methods=['POST']) 
def Stock_Select(): 
   if request.method == 'POST':
    stock = request.form.get('symb') 
    stockstdate = request.form.get('start')
    stockedate = request.form.get('end')

    stockv = yf.Ticker(stock)
    sdate = (stockstdate)
    edate = (stockedate)

    data_df = yf.download(stock, start=sdate, end=edate)

    #data_df.index = [x for x in range(1, len(data_df.values)+1)]
    #data_df.index.name = 'id'
    #data_df.index = data_df.index.map(str)
    #data_df=data_df.reset_index()

    data_df.columns = ["OPEN", "HIGH", "LOW", "CLOSE", "ADJ Close", "Volume"]
    data_df = data_df.round({"OPEN": 2, "HIGH": 2, "LOW": 2, "CLOSE": 2})


    profile = ProfileReport(data_df, title='Requested Stock Info', explorative=True)
    profile.to_file("/templates/searchedstock.html") 

