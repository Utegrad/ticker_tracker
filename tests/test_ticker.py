import io

from ticker.fetch import fetch_tickers_unique
from ticker.ticker import Ticker

csv_content_string = """<ticker>,<date>,<open>,<high>,<low>,<close>,<vol>
A,20190722,68.91,69.465,68.46,69.09,3103300
AA,20190722,23.18,23.3901,22.695,22.98,3719200
AAC,20190722,0.97,1.02,0.88,0.9099,127600
AAN,20190722,63.42,64.52,62.98,63.03,563500
AAP,20190722,157.28,160.17,157.24,158.9,840700
"""

csv_string_with_duplicates = """<ticker>,<date>,<open>,<high>,<low>,<close>,<vol>
A,20190722,68.91,69.465,68.46,69.09,3103300
AA,20190722,23.18,23.3901,22.695,22.98,3719200
AAC,20190722,0.97,1.02,0.88,0.9099,127600
AAN,20190722,63.42,64.52,62.98,63.03,563500
AAP,20190722,157.28,160.17,157.24,158.9,840700
AAN,20190722,63.42,64.52,62.98,63.03,563500
"""


def test_ticker_str_value():
    ticker = Ticker(ticker="ABC", name="A B C Company")
    assert ticker.__str__() == "ABC (A B C Company)"


def test_ticker_str_no_name():
    ticker = Ticker(ticker="ABC")
    assert ticker.__str__() == "ABC"


def test_tickers_from_csv():
    f = io.StringIO(csv_content_string)
    tickers = fetch_tickers_unique(f)
    assert any([i for i in tickers if i.ticker == "AAN"])


def test_tickers_from_csv_with_duplicates():
    f = io.StringIO(csv_string_with_duplicates)
    tickers = fetch_tickers_unique(f)
    assert len([i for i in tickers if i.ticker == "AAN"]) == 1
