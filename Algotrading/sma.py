import numpy as np
import pandas as pd
import yfinance as yf
from time import sleep
import datetime

principle = amount = 100000

df = pd.read_csv(r'C:\Users\naman\Documents\VS code\Algotrading\TATMOThistdata.csv') #historic data
bt = pd.read_csv(r'C:\Users\naman\Documents\VS code\Algotrading\TATMOT7d.csv') #backtesting dataset
df = df.drop(['Dividends', 'Stock Splits', 'Volume'], axis = 1)
bt = bt.drop(['Volume', 'Adj Close'], axis = 1)
sma = []
transactions = {'buy_time': None, 'buy_cost': None, 'sell_time': None, 'sell_cost': None}
t = pd.DataFrame(columns = ['buy_time', 'buy_cost', 'sell_time', 'sell_cost'])
for i in range(15, len(bt)):
    sma.append(round(sum(list(bt['Open'][i-15:i]))/15, 6))
    if len(sma) > 2:
        if sma[i-15] > sma[i-16] and sma[i-16] > sma[i-17] and transactions['buy_cost'] == None:
            transactions['buy_time'] = bt['Datetime'][i]
            transactions['buy_cost'] = round(bt['Open'][i], 6)
            volume = round(amount/bt['Open'][i], 6)
        
        if sma[i-15] < sma[i-16] and sma[i-16] < sma[i-17] and transactions['buy_cost'] != None:
            transactions['sell_time'] = bt['Datetime'][i]
            transactions['sell_cost'] = round(bt['Open'][i], 6)
            amount = round(volume * bt['Open'][i], 6)
            t = t.append(transactions, ignore_index = True)
            transactions = {'buy_time': None, 'buy_cost': None, 'sell_time': None, 'sell_cost': None}

print("Final amount =", amount)
print("Profit =", amount - principle)