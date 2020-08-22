from datetime import datetime as dt, timedelta
from flask import Flask, render_template

from execute_order import execute_order

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
@app.route('/index')
def index():
    initial_cash = 500
    asset_list = [['Spotify', 'SPOT', 2], ['Snapchat', 'SNAP', 0], ['Lululemon', 'Lulu', 3], ['Fitbit', 'FIT', 2]]
    asset_list = execute_order(initial_cash, asset_list)
    return render_template('index.html', title='Home', asset_list=asset_list)

app.run(debug=True)
