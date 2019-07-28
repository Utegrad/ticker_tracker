import os
from decimal import Decimal

from ticker.fetch import fetch_unique_tickers, dedupe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

in_files = ("NASDAQ_20190725.txt", "NYSE_20190725.txt")
out_file = "tickers.txt"
MIN_PRICE = 18
MAX_PRICE = 85


def gather_tickers():
    tickers = []
    for f in in_files:
        p = os.path.join(BASE_DIR, f)
        with open(p, "r") as csvfile:
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
    tickers = gather_tickers()
    out_path = os.path.join(BASE_DIR, out_file)
    with open(out_path, "w") as output:
        print(f"Writing output to: '{out_path}")
        for ticker in tickers:
            output.write(f"{ticker.ticker}\n")


if __name__ == "__main__":
    write_tickers()
