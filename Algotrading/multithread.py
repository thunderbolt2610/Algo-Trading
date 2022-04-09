import threading
import pandas as pd

ema_all = {'COALINDIA': {9:[], 20:[], 200:[]}, 'TITAN': {9:[], 20:[], 200:[]} ,'ITC': {9:[], 20:[], 200:[]} ,'HDFCLIFE': {9:[], 20:[], 200:[]}, 'RELIANCE': {9:[], 20:[], 200:[]}}

def preproc(t, df_old):
  sma=sum(list(df_old.tail(t)['Close']))/t
  return sma

def calcEMA(t, link, old_link, ticker):
    df=pd.read_csv(link)
    df_old=pd.read_csv(old_link)
    df_old=df_old.head(225)
    global ema_all
    closepts = list(df['Close'])
    emapts=[]
    for i in range(len(closepts)):
        if i==0:
            prev = preproc(t, df_old)
        ema = ((closepts[i] - prev)*(2/t))+prev
        prev=ema
        emapts.append(ema)
    ema_all[ticker][t].append(emapts)

def emathreads(t, link, old_link, ticker):
    tl = []
    for i in t:
        thread=threading.Thread(target=calcEMA,args=(i, link, old_link,ticker,))
        tl.append(thread)
        thread.start()

    for t in tl:
        t.join()

def calcSMA(link):
    amount = principle = 100000
    df = pd.read_csv(link)
    ema = {9:[], 20: [], 200: []}
    sma = []
    transactions = {'buy_time': None, 'buy_cost': None, 'sell_time': None, 'sell_cost': None}
    t = pd.DataFrame(columns = ['buy_time', 'buy_cost', 'sell_time', 'sell_cost'])
    for i in range(15, len(df)):
        sma.append(round(sum(list(df['Open'][i-15:i]))/15, 6))
        if len(sma) > 2:
            if sma[i-15] > sma[i-16] and sma[i-16] > sma[i-17] and transactions['buy_cost'] == None:
                transactions['buy_time'] = df['Datetime'][i]
                transactions['buy_cost'] = round(df['Open'][i], 6)
                volume = round(amount/df['Open'][i], 6)
            
            if sma[i-15] < sma[i-16] and sma[i-16] < sma[i-17] and transactions['buy_cost'] != None:
                transactions['sell_time'] = df['Datetime'][i]
                transactions['sell_cost'] = round(df['Open'][i], 6)
                amount = round(volume * df['Open'][i], 6)
                t.append(transactions, ignore_index = True)
                transactions = {'buy_time': None, 'buy_cost': None, 'sell_time': None, 'sell_cost': None}

       
    print("Amount: ", amount)
    print('Net: ', amount-principle)
  
if __name__ == "__main__":
    scrips=['COALINDIA','TITAN','ITC','HDFCLIFE','RELIANCE']
    threadlist=[]
    time = [9,20,200]
    for i in scrips:
        t=threading.Thread(target=emathreads,args=(time, r'C:\Users\naman\Documents\VS code\Algotrading\datasets\\'+ i +'.csv', r'C:\Users\naman\Documents\VS code\Algotrading\datasets\\'+ i +'preproc.csv',i,))
        threadlist.append(t)
        t.start()
        
    for t in threadlist:
        t.join()

    print(len(ema_all['COALINDIA'][200][0]))