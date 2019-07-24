from ticker.ticker import Ticker


def test_ticker_str_value():
    ticker = Ticker(ticker="ABC", name="A B C Company")
    assert ticker.__str__() == "ABC (A B C Company)"


def test_ticker_str_no_name():
    ticker = Ticker(ticker="ABC")
    assert ticker.__str__() == "ABC"
