from datetime import datetime

from ticker import Ticker


class EODData:
    def __init__(self):
        self.Ticker = Ticker()
        self._date = None
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.vol = None

    def __str__(self):
        return f"{self.ticker} - {self.date} open: {self.open} high: {self.high} low: {self.low} close: {self.close} vol: {self.vol}"

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
