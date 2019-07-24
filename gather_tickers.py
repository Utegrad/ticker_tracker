import os

from ticker.fetch import fetch_unique_tickers, dedupe

in_files = ('NASDAQ_20190722.txt', 'NYSE_20190722.txt')
out_file = 'tickers.txt'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def gather_tickers():
    tickers = []
    for f in in_files:
        p = os.path.join(BASE_DIR, f)
        with open(p, 'r') as csvfile:
            tickers.extend(fetch_unique_tickers(csvfile))
    all_tickers_unique = dedupe(tickers, 'ticker')
    all_tickers_unique.sort(key=lambda x: x.ticker)
    return all_tickers_unique


def write_tickers():
    tickers = gather_tickers()
    out_path = os.path.join(BASE_DIR, out_file)
    with open(out_path, 'w') as output:
        print(f"Writing output to: '{out_path}")
        for ticker in tickers:
            output.write(f"{ticker.ticker}\n")


if __name__ == '__main__':
    write_tickers()