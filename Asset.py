import numpy as np
from datetime import datetime as dt, timedelta

from load_data import load_data
class Asset():
    short_avg = 50
    long_avg = 200
    window = 365
    def __init__(self, name, ticker, start_date=dt.today()-timedelta(days=(long_avg + window)), end_date=dt.today()):
        self.price = load_data(ticker, start_date, end_date) #data on the price (high, low, and close)
        self.name = name #name of the stock (e.g. "Apple")

    def set_bollinger(self):
        bollinger_avg = 20 #number of days for the moving average
        std_limit = 2 #upper and lower limit for standard dev
        self.bollinger = self.price[['close']].copy()
        self.bollinger['tp'] = self.price[['high','low','close']].mean(axis=1) #typical price (see Investopedia)
        self.bollinger['ma'] = self.bollinger.tp.rolling('{}D'.format(bollinger_avg)).mean() #moving average
        std = self.bollinger.ma.std() #standard dev on MA
        self.bollinger['u_lim'] = self.bollinger.ma + (std * std_limit) #upper and lower limit
        self.bollinger['l_lim'] = self.bollinger.ma - (std * std_limit)

    def set_ma(self):
        self.ma = self.price[['close']].copy()
        self.ma['short_ma'] = self.ma[['close']].rolling('{}D'.format(self.short_avg)).mean() #short MA
        self.ma['long_ma'] = self.ma[['close']].rolling('{}D'.format(self.long_avg)).mean() #long MA

    def simple_long_ma_strat(self):
        signals = self.price[['close']].copy()
        signals['position'] = np.where(self.ma['close'] > self.ma['long_ma'], 1, 0)
        signals['position'] = signals['position'].diff() #1 for buy, -1 for sell
        return signals

    def golden_cross_strat(self):
        signals = self.price[['close']].copy()
        signals['position'] = np.where(self.ma['short_ma'] > self.ma['long_ma'], 1, 0)
        signals['position'] = signals['position'].diff() #1 for buy, -1 for sell
        return signals
    
    def bollinger_strat(self):
        signals = self.price[['close']].copy()
        signals['position'] = np.where(self.bollinger['close'] > self.bollinger['u_lim'], 1, 
                                       np.where(self.bollinger['close'] < self.bollinger['l_lim'], -1, 0))
        signals['position'] = signals['position'].diff() #1 for buy, -1 for sell
        return signals


    def execute_strats(self, initial_cash):
        strat_list = [self.simple_long_ma_strat, self.golden_cross_strat, self.bollinger_strat]
        strat_list = [self.simple_long_ma_strat]
        return_list = []
        for strat in strat_list:
            signals = strat()
            cash_list = [initial_cash] #cash levels
            for i in range(1,len(signals)):
                cash = cash_list[i-1] - (signals.close[i] * signals.position[i]) #reduces/increases cash for buy/sell
                if cash < 0:
                    cash = cash_list[i-1] #don't do anything that makes you short cash
                    signals.position.iloc[i] = 0
                cash_list.append(cash)
            signals['cash'] = cash_list
            final_return = signals['cash'].iloc[-1] + (signals['close'] * signals['position']).iloc[-1]
            