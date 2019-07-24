import csv

from .ticker import Ticker


def fetch_unique_tickers(f):
    """ Given a CSV io object return a set of unique Ticker() objects from <ticker> column where each

    :param f: io object with CSV content
    :return: list of unique Ticker() objects
    """
    ticker_objects = []
    all_ticker_strs = []

    reader = csv.DictReader(f)
    for row in reader:
        all_ticker_strs.append(row['<ticker>'])

    tickers_set = remove_duplicates(all_ticker_strs)

    for t in tickers_set:
        ticker = Ticker()
        ticker.ticker = t
        ticker_objects.append(ticker)

    return ticker_objects


def remove_duplicates(all_ticker_strs):
    tickers_set = set(all_ticker_strs)
    return tickers_set


def dedupe(objs, attrib):
    keys = []
    unique_objs = []
    for i in objs:
        if getattr(i, attrib) in keys:
            continue
        else:
            keys.append(getattr(i, attrib))
            unique_objs.append(i)
    return unique_objs
