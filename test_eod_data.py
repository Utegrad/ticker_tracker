from datetime import datetime
from decimal import *

import pytest

from eod_data import EODData
from ticker import Ticker

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
    eod._high = high
    eod._low = low
    eod._close = close
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


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_opening_is_decimal(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.opening = opening
    assert isinstance(eod.opening, Decimal)


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_opening_decimals_equal(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.opening = opening
    open_decimal = Decimal(opening)
    assert open_decimal == eod.opening


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_high_is_decimal_and_equal(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.high = high
    high_decimal = Decimal(high)
    assert isinstance(eod.high, Decimal)
    assert high_decimal == eod.high


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_low_is_decimal_and_equal(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.low = low
    low_decimal = Decimal(low)
    assert isinstance(eod.low, Decimal)
    assert low_decimal == eod.low


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_eod_close_is_decimal_and_equal(ticker, date, opening, high, low, close, vol):
    eod = EODData()
    eod.close = close
    close_decimal = Decimal(close)
    assert isinstance(eod.close, Decimal)
    assert close_decimal == eod.close


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_new_eod_Ticker_is_Ticker(ticker, date, opening, high, low, close, vol):
    eod = EODData.new_eod(ticker, date, opening, high, low, close, vol)
    assert isinstance(eod.Ticker, Ticker)
    assert eod.Ticker.ticker == ticker


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_new_eod_close_is_Decimal(ticker, date, opening, high, low, close, vol):
    eod = EODData.new_eod(ticker, date, opening, high, low, close, vol)
    assert isinstance(eod.close, Decimal)


@pytest.mark.parametrize('ticker, date, opening, high, low, close, vol', ticker_test_values)
def test_new_eod_close_value_equal_decimal(ticker, date, opening, high, low, close, vol):
    eod = EODData.new_eod(ticker, date, opening, high, low, close, vol)
    assert eod.close == Decimal(close)
