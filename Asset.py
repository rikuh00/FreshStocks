import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime as dt, timedelta

from load_data import load_data
class Asset():
    short_avg = 50
    long_avg = 200
    window = 365
    def __init__(self, name, ticker, start_date=dt.today()-timedelta(days=(long_avg + window)), end_date=dt.today()):
        self.price = load_data(ticker, start_date, end_date) #data on the price (high, low, and close)
        self.name = name #name of the stock (e.g. 'Apple')
        self.ticker = ticker # ticker

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

    def set_ema(self):
        look_back = 10
        self.ema = self.price[['close']].copy().ewm(span=look_back).mean() #Exponential WA
        self.ema.rename(columns={'close': 'ema'}, inplace=True)
        self.ema = self.price[['close']].join(self.ema, how='left')

    def exp_ma_strat(self):
        signals = self.price[['close']].copy()
        signals['position'] = np.where(self.ema['close'] > self.ema['ema'], 1, 0)
        signals['position'] = signals['position'].diff() #1 for buy, -1 for sell
        return signals

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

    def find_best_strat(self, initial_cash):
        self.set_ma()
        self.set_bollinger()
        self.set_ema()
        strat_dict = {self.simple_long_ma_strat:'Long MA', self.golden_cross_strat: 'Golden Cross', 
                        self.bollinger_strat: 'Bollinger', self.exp_ma_strat: 'Exponential WA'}
        strat = None
        final_std = None
        final_signal = None

        for _strat in strat_dict:
            _signal = _strat()
            cash_list = [initial_cash] #cash levels
            for i in range(1,len(_signal)):
                cash = cash_list[i-1] - (_signal.close[i] * _signal.position[i]) #reduces/increases cash for buy/sell
                cash_list.append(cash)
            _signal['cash'] = cash_list
            _signal['cash'].iloc[-1] += (_signal.position.sum() * _signal['close'].iloc[-1])
            _std = _signal.cash.std()
            if final_std is None or _std < final_std: #updating these variables to reflect the best strategy
                    final_std = _std
                    final_signal = _signal
                    strat = strat_dict[_strat]
            #final_signal.to_csv('{}.csv'.format(self.ticker))

        # Determining Buy/Sell Instructions based on the best strategy
        if strat == 'Long MA':
            curr_price = self.ma.close.iloc[-1]
            avg = self.ma.long_ma.iloc[-1]
            if curr_price > avg:
                return 'sell', avg
            elif curr_price < avg:
                return 'buy', avg
        
        elif strat == 'Golden Cross':
            curr_price = self.ma.close.iloc[-1]
            long_avg = self.ma.long_ma.iloc[-1]    
            short_avg = self.ma.short_ma.iloc[-1]
            low_end = min(short_avg, long_avg)
            high_end = max(short_avg, long_avg)
            if abs (curr_price - high_end) < abs(curr_price - low_end):
                return 'sell', high_end
            else:
                return 'buy', low_end
        
        elif strat == 'Bollinger':
            curr_price = self.bollinger.close.iloc[-1]
            u_lim = self.bollinger.u_lim.iloc[-1]    
            l_lim = self.bollinger.l_lim.iloc[-1]
            if abs(curr_price - u_lim) < abs(curr_price - l_lim):
                return 'sell', u_lim
            else:
                return 'buy', l_lim
        
        elif strat == 'Exponential WA':
            curr_price = self.ema.close.iloc[-1]
            price = curr_price #as a test
            ### put in code to compure w/ EWA
            if True: ###condition
                return 'sell', price
            else:
                return 'buy', price

    def execute_order(self, asset_level, initial_cash):
        instruction, price = self.find_best_strat(initial_cash)
        if instruction == 'sell':
            if asset_level > 0:
                return ('Sell at ${:.2f}'.format(price)) 
            else:
                return('We suggest that you wait until prices drop to buy this security.')
        elif instruction == 'buy':
            if initial_cash > price:
                num_shares = initial_cash // price
                if num_shares > 1:
                    return('Buy up to {:.0f} shares at ${:.2f} each'.format(num_shares, price))
                else:
                    return('Buy 1 share at ${:.2f}'.format(price))

    def plot_projections(self):
        plt.close()
        self.returns = self.price[['close']].copy()
        self.returns['returns'] = (self.returns.close/self.returns.close.shift(1)) - 1
        avg_return = self.returns.returns.mean()
        std_return = self.returns.returns.std()
        self.fut_returns = pd.DataFrame({'date':pd.date_range(start=dt.today(), end=dt.today()+timedelta(days=180))})
        self.fut_returns['max_return'] = [self.price['close'].iloc[-1] * ((1+(avg_return + 2*std_return))) ** i for i in range(len(self.fut_returns))]
        self.fut_returns.set_index('date', drop=True, inplace=True)
        self.fut_returns.plot()
        plt.savefig('static.png')