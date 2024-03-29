#!/usr/bin/env python3 
""" Functions to get and filter a list of tickers from the the .txt files from IN_FILES_DIR
    .txt files in input directory are a download of EOD csv data files from eoddata.com.
"""
import logging
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

logging.basicConfig(
    filename="gather_tickers.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def gather_tickers(input_files):
    """ Return a list of unique tickers from given input_files

    :return a list of unique tickers
    """
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
    unique_tickers = dedupe(tickers, "ticker")
    unique_tickers.sort(key=lambda x: x.ticker)
    return unique_tickers


def write_all_tickers():
    """ Write ALL_TICKERS_FILE with a list of tickers found in .txt files in the IN_FILES_DIR

    :return: None
    """
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

    :return: a generator for tickers that have been downloaded
    """
    download_dir = os.path.join(BASE_DIR, DOWNLOADED_DIR)
    for f in os.listdir(download_dir):
        if f.endswith(".csv"):
            yield f.replace(".csv", "").strip()


def filter_tickers():
    """ Write FILTERED_TICKERS_FILE with tickers that don't need to be downloaded again.

    :return: None
    """
    remaining_tickers = []
    downloaded_tickers = list(downloaded())
    with open(ALL_TICKERS_FILE, "r") as tickers:
        for t in tickers:
            t = t.strip()  # otherwise it has the newline character
            if has_punctuation(t):
                logger.info(F"Skipping {t} - has punctuation")
                continue
            elif t in downloaded_tickers:
                logger.info(f"Skipping {t} - already downloaded")
                continue
            else:
                logger.info(f"Including {t}")
                remaining_tickers.append(t)
    print(f"writing filtered tickers to '{FILTERED_TICKERS_FILE}'")
    with open(FILTERED_TICKERS_FILE, 'w') as f:
        for t in remaining_tickers:
            f.write(f"{t}\n")


if __name__ == "__main__":
    write_all_tickers()
    filter_tickers()
