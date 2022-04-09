import threading
import pandas as pd

def calc(link):
    amount = principle = 100000
    df = pd.read_csv(link)
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
    for i in scrips:
        t=threading.Thread(target=calc,args=(r'C:\Users\naman\Documents\VS code\Algotrading\\'+ i +'.csv',))
        threadlist.append(t)
        t.start()
        
    for t in threadlist:
        t.join()