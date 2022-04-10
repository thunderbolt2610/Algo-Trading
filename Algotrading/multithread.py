import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf

date = '2022-04-10'
x = datetime.datetime.now()
time = x.strftime("%X")
while (time >= '15:30:00'):
    #import dataset
    MSFT = yf.download(tickers='MSFT', period='3mo', interval='1d')
    INTC = yf.download(tickers='INTC', period='3mo', interval='1d')
    GOOG = yf.download(tickers='GOOG', period='3mo', interval='1d')
    AMZN = yf.download(tickers='AMZN', period='3mo', interval='1d')
    GAL = yf.download(tickers='GAL', period='3mo', interval='1d')
    DCM = yf.download(tickers='DCM', period='3mo', interval='1d')
    TATA = yf.download(tickers='TATAMOTORS.NS', period='3mo', interval='1d')
    ITC = yf.download(tickers='ITC', period='3mo', interval='1d')
    INFY = yf.download(tickers='INFY', period='3mo', interval='1d')
    AAPL = AAPL.reset_index()

    # compiling as dataset
    l = []
    l.append(AAPL.index)
    l.append(AAPL['Date'])
    l.append(AAPL['Adj Close'])
    l.append(AMZN['Adj Close'])
    l.append(GOOG['Adj Close'])
    l.append(INTC['Adj Close'])
    l.append(MSFT['Adj Close'])
    l.append(GAL['Adj Close'])
    l.append(DCM['Adj Close'])
    l.append(TATA['Adj Close'])
    l.append(ITC['Adj Close'])
    l.append(INFY['Adj Close'])

    # PIVOT DATASET
    df_pivot = pd.DataFrame(l).T
    df_pivot.columns = ['Symbol', 'Date', 'AAPL', 'AMZN', 'GOOG',
                        'INTC', 'MSFT', 'DCM', 'GAL', 'TATA', 'ITC', 'INFY']
    df_pivot = df_pivot.reset_index(drop=True)
    df_pivot = df_pivot[['AAPL', 'AMZN', 'GOOG', 'INTC', 'MSFT',
                         'DCM', 'GAL', 'TATA', 'ITC', 'INFY']].astype('float64')

    # CORR DATASET
    corr_df = df_pivot.corr(method='pearson')
    corr_df.head(10)

    # CALC RISK
    risk = corr_df.dropna()

    # Printing the top 5
    z = []
    for label, x, y in zip(risk.columns, risk.mean(), risk.std()):
        z.append([label, x, y])
    from operator import itemgetter
    z = sorted(z, key=itemgetter(1))
    print("The top 5 Companies to invest in:")
    for i in range(8, 3, -1):
        print(z[i][0])

while True:
    amount = 100000
    net = 0
    ema_all = {'COALINDIA': [], 'TITAN': [],
               'ITC': [], 'HDFCLIFE': [], 'RELIANCE': []}
    transaction = pd.DataFrame(columns=[
                               'ticker', 'buy_time', 'buy_cost', 'sell_time', 'sell_cost', 'volume', 'p/l'])

    def preproc(t, df_old):
        sma = sum(list(df_old.tail(t)['Close']))/t
        return sma

    def calcEMA(t, df_old, closepts, ticker):
        global ema_all
        emapts = []
        for i in range(len(closepts)):
            if i == 0:
                prev = preproc(t, df_old)
            ema = ((closepts[i] - prev)*(2/(t+1)))+prev
            prev = ema
            emapts.append(ema)
        ema_all[ticker].append(emapts)

    def calcSMA(link, ticker):
        amount = 100000
        global transaction, check
        df = pd.read_csv(link)
        sma = []
        transactions = {'ticker': None, 'buy_time': None, 'buy_cost': None,
                        'sell_time': None, 'sell_cost': None, 'volume': None, 'p/l': None}
        for i in range(15, len(df)):
            sma.append(round(sum(list(df['Open'][i-15:i]))/15, 6))
            if len(sma) > 2:
                if sma[i-15] > sma[i-16] and sma[i-16] > sma[i-17] and transactions['buy_cost'] == None:
                    transactions['buy_time'] = df['Datetime'][i]
                    transactions['buy_cost'] = round(df['Open'][i], 4)
                    volume = round(amount/df['Open'][i], 2)
                    transactions['volume'] = volume

                if sma[i-15] < sma[i-16] and sma[i-16] < sma[i-17] and transactions['buy_cost'] != None:
                    transactions['sell_time'] = df['Datetime'][i]
                    transactions['sell_cost'] = round(df['Open'][i], 4)
                    transactions['p/l'] = transactions['sell_cost'] - \
                        transactions['buy_cost']
                    transactions['ticker'] = ticker
                    amount = round(volume * df['Open'][i], 4)
                    transaction = transaction.append(
                        transactions, ignore_index=True)
                    transactions = {'ticker': None, 'buy_time': None, 'buy_cost': None,
                                    'sell_time': None, 'sell_cost': None, 'volume': None, 'p/l': None}

    def test(link, link_old, ticker):
        global amount, transaction
        df = pd.read_csv(link)
        df_old = pd.read_csv(link_old)
        closepts = list(df['Close'])
        calcEMA(9, df_old, closepts, ticker)
        calcEMA(20, df_old, closepts, ticker)
        transactions = {'ticker': None, 'buy_time': None, 'buy_cost': None,
                        'sell_time': None, 'sell_cost': None, 'volume': None, 'p/l': None}
        for i in range(len(ema_all[ticker][0])):
            if i > 1:
                if (ema_all[ticker][0][i-1]-ema_all[ticker][1][i-1]) > 0 and (ema_all[ticker][0][i]-ema_all[ticker][1][i]) < 0 and transactions['buy_cost'] == None:
                    transactions['buy_time'] = df['Datetime'][i]
                    transactions['buy_cost'] = round(df['Close'][i], 2)
                    volume = round(amount/df['Close'][i], 2)
                    transactions['volume'] = volume

                if (ema_all[ticker][0][i-1]-ema_all[ticker][1][i-1]) < 0 and (ema_all[ticker][0][i]-ema_all[ticker][1][i]) > 0 and transactions['buy_cost'] != None:
                    transactions['sell_time'] = df['Datetime'][i]
                    transactions['sell_cost'] = round(df['Close'][i], 2)
                    amount = round(volume * df['Open'][i], 1)
                    transactions['p/l'] = transactions['sell_cost'] - \
                        transactions['buy_cost']
                    transactions['ticker'] = ticker
                    transaction = transaction.append(
                        transactions, ignore_index=True)
                    transactions = {'ticker': None, 'buy_time': None, 'buy_cost': None,
                                    'sell_time': None, 'sell_cost': None, 'volume': None, 'p/l': None}

    scrips = ['COALINDIA', 'TITAN', 'ITC', 'HDFCLIFE', 'RELIANCE']
    for i in range(len(scrips)):
        test(r'C:\Users\naman\Documents\GitHub\Algo-Trading\Algotrading\datasets\\' +
             scrips[i] + '.csv', r'C:\Users\naman\Documents\GitHub\Algo-Trading\Algotrading\datasets\\' + scrips[i] + '.csv', scrips[i])
        # threadList=[]
        # for scrip in scrips:
        #     t=threading.Thread(target=test,args=(r'C:\Users\naman\Documents\GitHub\Algo-Trading\Algotrading\datasets\\' + scrip + '.csv', r'C:\Users\naman\Documents\GitHub\Algo-Trading\Algotrading\datasets\\' + scrip +'.csv',scrip,))
        #     t.start()
        #     threadList.append(t)

        # for t in threadList:
        #     t.join()

    for i in range(len(transaction)):
        net = net + transaction['volume'][i]*transaction['p/l'][i]
    print(transaction)
    print('Net:', net)
    break
