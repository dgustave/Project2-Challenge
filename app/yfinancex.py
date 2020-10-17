
import yfinance as yf
import pandas as pd
from datetime import date, timedelta, datetime as dt
import numpy as np
import matplotlib.pyplot as plt 
from yahoo_fin.stock_info import get_analysts_info
from yahoo_fin.stock_info import *
from pymongo import MongoClient
import numpy as np



client =  MongoClient("mongodb://localhost:27017")



def stockData(symbol):
    db = client['investopedia']
    db.list_collection_names()
    col = db.sector_stock_list
    top_stocks = col.find_one()
    top_list = [collect for collect in top_stocks['Sector Stocks']]
    ticks = yf.Ticker(symbol)
    currentDate = date.today()
    enddate = currentDate.strftime('%Y-%m-%d')
    four_yrs = currentDate - timedelta(days=2016)
    startdate = four_yrs.strftime('%Y-%m-%d')
    ydata_df = yf.download(symbol, start=startdate, end=enddate)
    ydata_df.columns = ["OPEN", "HIGH", "LOW", "CLOSE", "Adj Close", "Volume"]
    daily_close = ydata_df[['Adj Close']]
    daily_pct_change = daily_close.pct_change()
    daily_pct_change.fillna(0, inplace=True)
    daily_pct_change
    min_periods = 2

    # Calculate the volatility
    vol = (daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods))
    vol.columns = ["VOLATILITY"]
    vol.fillna(0, inplace=True)
    out = ticks.info.get('sharesOutstanding')
    daily_turnover = ydata_df[['Volume']]
    turnover = (daily_turnover/out) 
    turnover.columns = ["TURNOVER"]

    ydata_df["TURNOVER"] = turnover["TURNOVER"]
    ydata_df["VOLATILITY"] = vol["VOLATILITY"]
    data_df = ydata_df.drop(columns = ["Adj Close", "Volume"])

    df = data_df.reset_index()
    df = df.rename(columns = {"Date": "TIMESTAMP"})

    new_df = df.round({"OPEN": 2, "HIGH": 2, "LOW": 2, "CLOSE": 2})
    new_df


    TIMESTAMP = new_df["TIMESTAMP"].to_list()
    OPEN = new_df["OPEN"].to_list()
    HIGH = new_df["HIGH"].to_list()
    LOW = new_df["LOW"].to_list()
    CLOSE = new_df["CLOSE"].to_list()
    TURNOVER = new_df["TURNOVER"].to_list()
    VOLATILITY = new_df["VOLATILITY"].to_list()
    vol_dict = {"TIMESTAMP": TIMESTAMP, "OPEN": OPEN, "HIGH": HIGH, "LOW ": LOW , "CLOSE": CLOSE, "TURNOVER": TURNOVER, "VOLATILITY": VOLATILITY,}

    db = client['yfinancing']
    yfinancing_collection = db[symbol]
    yfinancing_collection.update_one({}, {"$set": vol_dict}, upsert= True)

    new_df.to_csv(f"../data/processed/{symbol}.csv", index = False)



stockData('CVS')  
stockData('BIIB')  
stockData('BIO')  
stockData('NEM')  
stockData('PODD')  
stockData('PWR')  
stockData('SMG')  
stockData('TSLA')  
stockData('XRX')  
stockData('NCR')  
stockData('ENR')  
stockData('LVGO')  
