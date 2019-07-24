from datetime import datetime
from decimal import Decimal

from ticker import Ticker


class EODData:
    def __init__(self):
        self.Ticker = Ticker()
        self._date = None
        self._open = None
        self._close = None
        self._high = None
        self._low = None
        self.vol = None

    def __str__(self):
        return f"{self.ticker} - {self.date} open: {self.opening} high: {self.high} low: {self.low} close: {self.close} vol: {self.vol}"

    @property
    def ticker(self):
        return self.Ticker.ticker

    @ticker.setter
    def ticker(self, value):
        self.Ticker.ticker = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        try:
            self._date = datetime.strptime(value, '%Y%m%d')
        except Exception as e:
            raise e

    @property
    def opening(self):
        return self._open

    @opening.setter
    def opening(self, value):
        try:
            self._open = Decimal(value)
        except Exception as e:
            raise e

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, value):
        try:
            self._high = Decimal(value)
        except Exception as e:
            raise e

    @property
    def low(self):
        return self._low

    @low.setter
    def low(self, value):
        try:
            self._low = Decimal(value)
        except Exception as e:
            raise e

    @property
    def close(self):
        return self._close

    @close.setter
    def close(self, value):
        try:
            self._close = Decimal(value)
        except Exception as e:
            raise e

    @classmethod
    def new_eod(cls, ticker, date, opening, high, low, close, vol):
        eod = cls()
        eod.ticker = ticker
        eod.date = date
        eod.opening = opening
        eod.high = high
        eod.low = low
        eod.close = close
        eod.vol = vol
        return eod
