class Ticker:
    def __init__(self, ticker=None, name=None):
        self.ticker = ticker
        self.name = name

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.ticker})"
        else:
            return f"{self.ticker}"

    def __repr__(self):
        return f"Ticker()"
