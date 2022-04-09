import numpy as np
import pandas as pd
import yfinance as yf
from time import sleep
import datetime
tickers=['COALINDIA','TITAN','ITC','HDFCLIFE','RELIANCE']
for i in tickers:
    data = yf.download(tickers=i+'.NS', start="2022-03-28", end="2022-03-31", interval='5m')
    data.to_csv(i+'preproc.csv')
    # data = yf.download(tickers=i+'.NS', period='7d', interval='5m')
    # data.to_csv(i+'.csv')
