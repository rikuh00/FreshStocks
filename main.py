from datetime import datetime as dt, timedelta
from flask import Flask, render_template, redirect
from form_config import Config
from execute_order import execute_order
from stock_form import StockForm
from welcome_form import WelcomeForm
from stock_suggestion import interest_stocks
from stock_suggestion import interest_function

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config.from_object(Config)
avail_cash = 0
@app.route('/home', methods=['GET', 'POST'])
def home():
    form =  WelcomeForm()
    if form.validate_on_submit():
        avail_cash = form.cash.data
        return redirect('/index')
    return render_template('home.html', title='Welcome!', form=form)

    # don't need to test request.method == 'GET'
    return render_template('survey.html')
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    initial_cash = 500
    asset_list = [['Spotify', 'SPOT', 2], ['Snapchat', 'SNAP', 0], ['Lululemon', 'Lulu', 3], ['Fitbit', 'FIT', 2]]
    asset_list = execute_order(initial_cash, asset_list)

    form = StockForm()

    if form.validate_on_submit():
        return redirect('/interests')
    return render_template('index.html', title='Home', asset_list=asset_list, form=form)

@app.route('/interests', methods=['GET', 'POST'])
def interests_page():
    '''

    :return:
    '''
    initial_cash = 500
    form = StockForm()
    music_list = execute_order(initial_cash, interest_stocks['Music'])
    fashion_list = execute_order(initial_cash, interest_stocks['Fashion'])
    entertainment_list = execute_order(initial_cash, interest_stocks['Entertainment'])
    sports_list = execute_order(initial_cash, interest_stocks['Sports'])
    technology_list = execute_order(initial_cash, interest_stocks['Technology'])
    print(interest_stocks)

    if form.validate_on_submit():
        return redirect('/index')

    return render_template('interests.html', title='Interests',
                           music_list=music_list,
                           fashion_list=fashion_list,
                           entertainment_list=entertainment_list,
                           sports_list=sports_list,
                           technology_list=technology_list,
                           form=form)


app.run(debug=True)

