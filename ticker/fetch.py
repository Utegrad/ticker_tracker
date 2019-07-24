import csv

from .ticker import Ticker


def fetch_tickers_unique(f):
    """ Given a CSV object return a set of Ticker() objects from ticker column

    :param f:
    :return:
    """
    ticker_objects = []
    all_ticker_strs = []
    reader = csv.DictReader(f)
    for row in reader:
        all_ticker_strs.append(row['<ticker>'])
    tickers_set = set(all_ticker_strs)
    for t in tickers_set:
        ticker = Ticker()
        ticker.ticker = t
        ticker_objects.append(ticker)
    return ticker_objects
