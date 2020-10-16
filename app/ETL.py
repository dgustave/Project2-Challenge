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






def Stock_Select(request): 
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
    data_df=data_df.reset_index()

    data_df.columns = ["Date", "OPEN", "HIGH", "LOW", "CLOSE", "ADJ Close", "Volume"]
    data_df = data_df.round({"OPEN": 2, "HIGH": 2, "LOW": 2, "CLOSE": 2})

    data_df.to_csv('../data/StockETL.csv', index = True)
   

    stock_json = data_df.to_json(orient="records", date_format='iso')
    final_json = json.loads(stock_json)
   json.dumps(stock_json, indent=0) 
   with open('../data/Searchedstock.json', 'w') as json_file:
    json.dump(final_json, json_file)

