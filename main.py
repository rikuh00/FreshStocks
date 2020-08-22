from datetime import datetime as dt, timedelta
from flask import Flask

from Asset import Asset

app = Flask(__name__)

if __name__ == '__main__':
    initial_cash = 500
    asset_level = 2
    data = Asset('TESLA', 'TSLA')
    data.set_ema()
    data.exp_ma_strat()
    data.execute_order(asset_level, initial_cash)

@app.route('/')
def hello():
    #Put in HTML here
    return 'Hi there!'