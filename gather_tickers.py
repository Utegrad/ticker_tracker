""" Functions to get and filter a list of tickers from the the .txt files from IN_FILES_DIR
    .txt files in input directory are a download of EOD csv data files from eoddata.com.
"""
import os
from decimal import Decimal

from helpers import ls_l
from ticker.fetch import fetch_unique_tickers, dedupe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IN_FILES_DIR = 'input'
OUT_FILE = "tickers.txt"
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


def write_tickers():
    input_files = (f for f in ls_l(os.path.join(BASE_DIR, IN_FILES_DIR)) if f.endswith('.txt'))
    tickers = gather_tickers(input_files)
    out_path = os.path.join(BASE_DIR, OUT_FILE)
    with open(out_path, "w") as output:
        print(f"Writing output to: '{out_path}")
        for ticker in tickers:
            output.write(f"{ticker.ticker}\n")


if __name__ == "__main__":
    write_tickers()
