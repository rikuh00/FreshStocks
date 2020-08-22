from datetime import datetime as dt, timedelta
from flask import Flask, render_template

from Asset import Asset
def execute_order():
    initial_cash = 500
    asset_level = 2
    asset = Asset('Spotify', 'SPOT')
    asset.set_ema()
    asset.exp_ma_strat()
    order = asset.execute_order(asset_level, initial_cash)
    return asset, order

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    asset, order = execute_order()
    return render_template('index.html', title='Home', asset=asset, order=order)

app.run(debug=True)
