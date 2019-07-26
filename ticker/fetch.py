import csv
import decimal

from .ticker import Ticker


def fetch_unique_tickers(f, fn=None):
    """ Given a CSV io object return a set of unique Ticker() objects from <ticker> column where each

    :param fn: filter function to limit which tickers are returned
    :param f: io object with CSV content
    :return: list of unique Ticker() objects
    """
    ticker_objects = []

    reader = csv.DictReader(f)
    for row in reader:
        if fn:
            try:
                if fn(row):
                    ticker_objects.append(Ticker(ticker=row["<ticker>"]))
                else:
                    continue
            except TypeError:
                continue  # appears to encounter a type error at the end of the csv file
            except decimal.InvalidOperation:
                continue  # encountered when a filtered CSV field is empty.  Skip it since it's empty
            except Exception as e:
                raise e
        else:
            ticker_objects.append(Ticker(ticker=row["<ticker>"]))

    tickers_set = dedupe(ticker_objects, "ticker")

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
