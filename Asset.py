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
        std_limit = 1 #upper and lower limit for standard dev
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
        strat_dict = {self.simple_long_ma_strat:'Long MA', self.golden_cross_strat: 'Golden Cross', self.bollinger_strat: 'Bollinger'}
        strat = None
        final_return = None
        final_signal = None

        for _strat in strat_dict:
            _signal = _strat()
            cash_list = [initial_cash] #cash levels
            for i in range(1,len(_signal)):
                cash = cash_list[i-1] - (_signal.close[i] * _signal.position[i]) #reduces/increases cash for buy/sell
                cash_list.append(cash)
            _signal['cash'] = cash_list
            _return = _signal['cash'].iloc[-1] + ((_signal['close'] * _signal['position']).iloc[-1])
            if final_return is None or _return > final_return:
                    final_return = _return
                    final_signal = _signal
                    strat = strat_dict[_strat]
        print('The best strategy is {}'.format(strat))
        if strat == 'Long MA':
            curr_price = self.ma.close.iloc[-1]
            avg = self.ma.long_ma.iloc[-1]
            if curr_price > avg:
                print('Sell {} at ${:.2f}'.format(self.name, avg))
            elif curr_price < avg:
                print('Buy {} at ${:.2f}'.format(self.name, avg))
        
        elif strat == 'Golden Cross':
            curr_price = self.ma.close.iloc[-1]
            long_avg = self.ma.long_ma.iloc[-1]    
            short_avg = self.ma.short_ma.iloc[-1]
            print('Buy at ${:.2f} or Sell at ${:.2f}'.format(min(long_avg, short_avg), max(long_avg, short_avg)))
        
        elif strat == 'Bollinger':
            curr_price = self.bollinger.close.iloc[-1]
            u_lim = self.bollinger.u_lim.iloc[-1]    
            l_lim = self.bollinger.l_lim.iloc[-1]
            if abs(curr_price - u_lim) > abs(curr_price - l_lim):
                print('Buy at ${:.2f}'.format(l_lim))
            else:
                print('Sell at ${:.2f}'.format(u_lim))         