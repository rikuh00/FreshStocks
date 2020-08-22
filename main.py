from datetime import datetime as dt, timedelta
from flask import Flask, render_template

from Asset import Asset
def execute_order():
    initial_cash = 500
    asset_level = 2
    tsla = Asset('TESLA', 'TSLA')
    tsla.set_ema()
    tsla.exp_ma_strat()
    tsla.execute_order(asset_level, initial_cash)
    return tsla

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', asset=execute_order())

app.run(debug=True)
