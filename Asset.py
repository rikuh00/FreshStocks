from datetime import datetime as dt, timedelta

from load_data import load_data
class Asset():
    short_avg = 50
    long_avg = 200
    window = 365
    def __init__(self, name, ticker, start_date=dt.today()-timedelta(long_avg + window), end_date=dt.today()):
        self.close = load_data(ticker, start_date, end_date)
        self.name = name

    def set_bollinger(self):
        bollinger_avg = 20
        self.bollinger = self.close.copy()
        self.bollinger['avg'] = self.bollinger.close.rolling('{}D'.format(bollinger_avg)).mean()
        
        #self.bollinger['upper_limit'] = 
    def set_ma(self):
        self.ma = self.close.copy()
        self.ma['short_ma'] = self.ma[['close']].rolling('{}D'.format(self.short_avg)).mean()
        self.ma['long_ma'] = self.ma[['close']].rolling('{}D'.format(self.long_avg)).mean()
