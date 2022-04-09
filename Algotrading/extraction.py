import numpy as np
import pandas as pd
import yfinance as yf
from time import sleep
import datetime

principle = 100000

df = pd.read_csv(r'C:\Users\naman\Documents\VS code\Algotrading\TATMOThistdata.csv')
value = pd.read_csv(r'C:\Users\naman\Documents\VS code\Algotrading\TATMOT7d.csv')
df = df.drop(['Dividends', 'Stock Splits', 'Volume'], axis = 1)
df['pos diff'] = 0.0
df['neg diff'] = 0.0
for i in range(len(df)):
    df['pos diff'][i] = df['High'][i] - df['Open'][i]
    df['neg diff'][i] = df['Open'][i] - df['Low'][i]
avg = dict(df.mean(axis=0).round(6))
avg['pos diff'] = 0.9*avg['pos diff']
avg['neg diff'] = 0.7*avg['neg diff']
print(avg)

for i in range(7):
    tempval = value[i*375:i*375+375]
    x = 0
    amount = 0
    sellprice = 0
    #live data extraction
    print("Principle: ", principle)
    for index, data in tempval.iterrows():
        x+=1
        #purchase shares based on opening price
        # if datetime.datetime.now().strftime("%H:%M") == "9:15":
        if x == 1:
            noofshares = principle//data['Open']
            remsum = round(principle%data['Open'], 3)
            buyprice = data['Open']
            print("Shares purchased: ", noofshares)
            print("Money remaining: ", remsum)
            print('Buying price: ', buyprice)

        #check live data
        if data['Open'] >= buyprice + avg['pos diff']:
            amount = remsum + noofshares*data['Open']
            print("Amount: ",  amount)
            print("time of sell: ", data['Datetime'])
            sellprice = data['Open']
            noofshares = 0
            break
        elif data['Open'] <= buyprice - avg['neg diff']:
            amount = remsum + noofshares*data['Open']
            noofshares = 0
            sellprice = data['Open']
            print("Amount: ", amount)
            print("time of sell: ", data['Datetime'])
            break
        elif x == 371:
            amount = remsum + noofshares*data['Open']
            noofshares = 0
            sellprice = data['Open']
            print("Amount: ", amount)
            print("time of sell: ", data['Datetime'])
            break
    gains = amount - principle
    # sleep(60)
    print("Selling Price: ", sellprice)
    print("Gains: ", gains)
    principle = amount
    print("\n\n")