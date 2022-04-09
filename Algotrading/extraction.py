import numpy as np
import pandas as pd
import yfinance as yf
from time import sleep
import datetime

data = yf.download(tickers='TATAMOTORS.NS', period='7d', interval='1m')
print(data)