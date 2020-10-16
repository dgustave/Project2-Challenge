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
import plotly.graph_objects as go






def Stock_Select(request): 
   if request.method == 'POST':
    stock = request.form.get('symb') 
    stockstdate = request.form.get('start')
    stockedate = request.form.get('end')

    stockv = yf.Ticker(stock)
    sdate = (stockstdate)
    edate = (stockedate)

    data_df = yf.download(stock, start=sdate, end=edate)
    data_df2 = data_df.reset_index(drop=False)
    #data_df.index = [x for x in range(1, len(data_df.values)+1)]
    #data_df.index.name = 'id'
    #data_df.index = data_df.index.map(str)

    data_df2.columns = [ "Date", "OPEN", "HIGH", "LOW", "CLOSE", "ADJ Close", "Volume"]
    data_df2 = data_df2.round({"OPEN": 2, "HIGH": 2, "LOW": 2, "CLOSE": 2})


    fig = go.Figure(data=[go.Candlestick(x=data_df2["Date"],
                open=data_df2['OPEN'], high=data_df2['HIGH'],
                low=data_df2['LOW'], close=data_df2['CLOSE'])
                      ])

    fig.update_layout(
     title="Requested Stock Info",
     yaxis_title=f"{stock}"
    )

    fig.update_layout(autosize=False, width=800, height=500)

    fig.write_html('templates/StockETL.html')

    data_df2.to_csv('../data/StockETL.csv', index = True)
   

    stock_json = data_df2.to_json(orient="records", date_format='iso')
    final_json = json.loads(stock_json)
   json.dumps(stock_json, indent=0) 
   with open('../data/Searchedstock.json', 'w') as json_file:
    json.dump(final_json, json_file)

