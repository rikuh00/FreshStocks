#%% IMPORTS
import lxml
import pandas as pd
import requests
import time
import numpy as np
from datetime import datetime, timedelta 
from lxml import html

#%% SUBFUNCTIONS
# Format Date
def _format_date(date):
    date = date.timetuple()
    date = time.mktime(date)
    date = int(date)
    date = str(date)
    return date

# Create Partitions (100 Days Each)
def _create_date_partitions(start_date, end_date):
    date_partition_list = []
    end_100days = end_date
    start_100days = end_date
    while (start_100days - start_date) > timedelta(days=100):
        start_100days = end_100days - timedelta(days=100)
        date_partition_list.append((_format_date(start_100days), _format_date(end_100days)))
        end_100days = start_100days
    end_100days = start_100days
    start_100days = start_date
    date_partition_list.append((_format_date(start_100days), _format_date(end_100days)))
    return date_partition_list

# Create a Subdomain
def _create_subdomain(ticker, start, end, filter='history'):
    subdomain='/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter={3}&frequency=1d'
    subdomain = subdomain.format(ticker, start, end, filter)
    return subdomain

# Create a Header based on the Subdomain
def _create_header(subdomain):
    headers =  {"authority": "finance.yahoo.com",
            "method": "GET",
            "path": subdomain,
            "scheme": "https",
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "cookie": "Cookie:identifier",
            "dnt": "1",
            "pragma": "no-cache",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64)"}
    return headers

# Scrape a Webpage (Single Loop)
def _scrape_page_helper(ticker, begin_100days, end_100days):
    BASE_URL = 'https://finance.yahoo.com'
    subdomain = _create_subdomain(ticker, begin_100days, end_100days)
    url = BASE_URL + subdomain
    header = _create_header(subdomain)
    page = requests.get(url, headers=header)
    element_html = html.fromstring(page.content)
    table = element_html.xpath('//table')
    table_tree = lxml.etree.tostring(table[0], method='xml')
    df = (pd.read_html(table_tree))[0]
    df.drop(index = len(df)-1, inplace=True)
    return df

#%% SCRAPE WEBPAGE
def load_data(ticker, start_date, end_date):
    date_partition_list = _create_date_partitions(start_date, end_date)
    df = pd.DataFrame()
    for date_partition in date_partition_list:
        df_temp = _scrape_page_helper(ticker, begin_100days=date_partition[0], end_100days=date_partition[1])
        df = pd.concat([df, df_temp])
    df.columns = ['date', 'open', 'high', 'low', 'Close', 'adj Close', 'volume']
    df.date = df.date.apply(lambda x: datetime.strptime(x, r'%b %d, %Y'))
    df.replace('-', np.nan, inplace=True)
    df.fillna(method='ffill', inplace=True)
    df = df[pd.to_numeric(df['Close'], errors='coerce').notnull()]
    df.set_index('date', drop=True, inplace=True)
    df.sort_index(inplace=True)
    df = df.astype(float)
    df = df[['high','low','Close']]
    df.rename(columns={'Close':'close'}, inplace=True)
    return df

#%% MAIN
if __name__ == '__main__':
    ticker = 'VGRO.TO'
    name = 'VGRO'
    end_date = datetime.now()
    start_date = end_date - timedelta(days=50)
    df = load_data(ticker, start_date, end_date)
    print(df.head())