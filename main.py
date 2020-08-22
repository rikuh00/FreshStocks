from datetime import datetime as dt, timedelta
from Asset import Asset
if __name__ == '__main__':
    end_date = dt.today()
    start_date = end_date - timedelta(days=50)
    lulu = Asset('Lululemon','LULU', start_date, end_date)
    print(lulu.name)
    #print(lulu.close.tail())
    lulu.set_bollinger()
    #print(lulu.ma.tail())