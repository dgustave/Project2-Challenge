import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from flask import request
from flask import Flask 
from flask import request 
import datetime



@app.route('/Stock Select', methods=['POST', 'GET']) 
def Stock Select() 
	if request.method == 'POST': 
		stock = request.form.get('symb') 
		stockstdate = request.form.get('start') 
        stockedate = request.form.get('end')
		 
	else: 
	 return "<p>Please Try Again.</p>"

stocksdate2 = stocksdate.strftime('%Y-%m-%d')
stockedate2 = stockedate.strftime('%m-%d-%Y')

stockv = yf.Ticker(stock)
sdate = (stockstdate)
edate = (stockedate)

data_df = yf.download(stock, start=sdate, end=edate)

data_df.index = [x for x in range(1, len(data_df.values)+1)]
data_df.index.name = 'id'
data_df.index = data_df.index.map(str)

data_df.to_csv('../../data/external/StockETL.csv', index = False)