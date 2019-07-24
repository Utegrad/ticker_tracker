import csv

from .ticker import Ticker


def fetch_unique_tickers(f):
    """ Given a CSV io object return a set of unique Ticker() objects from <ticker> column where each

    :param f: io object with CSV content
    :return: list of unique Ticker() objects
    """
    ticker_objects = []

    reader = csv.DictReader(f)
    for row in reader:
        ticker_objects.append(Ticker(ticker=row['<ticker>']))

    tickers_set = dedupe(ticker_objects, 'ticker')

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
