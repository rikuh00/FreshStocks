from datetime import datetime as dt, timedelta
from Asset import Asset
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':

    lulu = Asset('Lululemon','LULU')
    #print(lulu.close.tail())
    lulu.set_ma()
    lulu.set_bollinger()
    lulu.execute_strats(500)
    #print(lulu.ma.tail())

@app.route('/')
def hello():
    #Put in HTML here
    return 'Hi there!'