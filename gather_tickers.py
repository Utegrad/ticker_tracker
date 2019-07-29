""" Functions to get and filter a list of tickers from the the .txt files from IN_FILES_DIR
    .txt files in input directory are a download of EOD csv data files from eoddata.com.
"""
import os
from decimal import Decimal

from helpers import ls_l, has_punctuation
from ticker.fetch import fetch_unique_tickers, dedupe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IN_FILES_DIR = "input"
DOWNLOADED_DIR = "downloads"
ALL_TICKERS_FILE = "tickers.txt"
FILTERED_TICKERS_FILE = "filtered_tickers.txt"
MIN_PRICE = 15
MAX_PRICE = 1200


def gather_tickers(input_files):
    tickers = []
    for f in input_files:
        with open(f, "r") as csvfile:
            tickers.extend(
                fetch_unique_tickers(
                    csvfile,
                    lambda row: True
                    if MIN_PRICE < Decimal(row["<close>"]) < MAX_PRICE
                    else False,
                )
            )
    all_tickers_unique = dedupe(tickers, "ticker")
    all_tickers_unique.sort(key=lambda x: x.ticker)
    return all_tickers_unique


def all_tickers():
    input_files = (
        f for f in ls_l(os.path.join(BASE_DIR, IN_FILES_DIR)) if f.endswith(".txt")
    )
    tickers = gather_tickers(input_files)
    out_path = os.path.join(BASE_DIR, ALL_TICKERS_FILE)
    with open(out_path, "w") as output:
        print(f"Writing output to: '{out_path}")
        for ticker in tickers:
            output.write(f"{ticker.ticker}\n")


def downloaded():
    """ get the tickers that have already been downloaded

    :return: an iterable with tickers that have been downloaded
    """
    download_dir = os.path.join(BASE_DIR, DOWNLOADED_DIR)
    for f in os.listdir(download_dir):
        if f.endswith(".csv"):
            yield f.replace(".csv", "").strip()


def filter_tickers():
    """ Filter and rewrite tickers.txt that aren't going to be downloaded again.

    :return: None
    """
    remaining_tickers = []
    downloaded_tickers = list(downloaded())
    with open(ALL_TICKERS_FILE, "r") as tickers:
        for t in tickers:
            t = t.strip()  # otherwise it has the newline character
            if has_punctuation(t):
                continue
            elif t in downloaded_tickers:
                continue
            else:
                remaining_tickers.append(t)
    with open(FILTERED_TICKERS_FILE, 'w') as f:
        for t in remaining_tickers:
            f.write(f"{t}\n")


if __name__ == "__main__":
    filter_tickers()
