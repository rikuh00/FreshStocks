from datetime import datetime as dt, timedelta

from load_data import load_data
class Asset():
    short_avg = 50
    long_avg = 200
    window = 365
    def __init__(self, name, ticker, start_date=dt.today()-timedelta(long_avg + window), end_date=dt.today()):
        self.price = load_data(ticker, start_date, end_date)
        self.name = name

    def set_bollinger(self):
        bollinger_avg = 20
        std_limit = 2
        self.bollinger = self.price[['close']].copy()
        self.bollinger['tp'] = self.price[['high','low','close']].mean(axis=1)
        self.bollinger['ma'] = self.bollinger.tp.rolling('{}D'.format(bollinger_avg)).mean()
        std = self.bollinger.ma.std()
        self.bollinger['u_lim'] = self.bollinger.ma + (std * std_limit)
        self.bollinger['l_lim'] = self.bollinger.ma - (std * std_limit)
        print(self.bollinger.head())
    def set_ma(self):
        self.ma = self.price[['close']].copy()
        self.ma['short_ma'] = self.ma[['close']].rolling('{}D'.format(self.short_avg)).mean()
        self.ma['long_ma'] = self.ma[['close']].rolling('{}D'.format(self.long_avg)).mean()
