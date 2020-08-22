from load_data import load_data
class Asset():
    def __init__(self, name, ticker, start_date, end_date):
        self.close = load_data(ticker, start_date, end_date)
        self.name = name


