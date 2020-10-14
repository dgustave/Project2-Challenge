# Import Dependencies 
from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
from flask_assets import Environment, Bundle
from flask_scss import Scss
from datetime import datetime
import os



# Create an instance of Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

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

    data_df.index = [x for x in range(1, len(data_df.values)+1)]
    data_df.index.name = 'id'
    data_df.index = data_df.index.map(str)


    #data_df.to_csv('../data/external/StockETL.csv', index = False)
    #return redirect('index.html')

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


