from datetime import datetime
from decimal import *

import pytest

from eod_data import EODData

ticker_test_values = [
    ('abc', '20190101', '12.34', '13.45', '11.45', '12.45', 100000),
    ('AA', '20190722', 23.18, 23.3901, 22.695, 22.98, 3719200),
]


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_ticker_str_value(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.ticker = ticker
    eod.date = date
    eod.open = opening
    eod.high = high
    eod.low = low
    eod.close = close
    eod.vol = vol
    assert eod.ticker == ticker


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_vol_is_int(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.vol = vol
    assert isinstance(eod.vol, int)


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_date_is_datetime(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.date = date
    assert isinstance(eod.date, datetime)
