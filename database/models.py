from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

Base = declarative_base()


class Ticker(Base):
    __tablename__ = "tickers"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=64), nullable=True)
    ticker = Column(String(length=8), nullable=False, index=True, unique=True)

    prices = relationship("Price", back_populates="ticker")

    def __repr__(self):
        return f"<Ticker('{self.ticker}')>"

    def __str__(self):        return f"{self.ticker}"


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id'), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(DOUBLE, nullable=False)
    high = Column(DOUBLE, nullable=False)
    low = Column(DOUBLE, nullable=False)
    close = Column(DOUBLE, nullable=False)
    adj_close = Column(DOUBLE, nullable=False)
    volume = Column(Integer, nullable=False)

    ticker = relationship("Ticker", back_populates="prices")

    def __repr__(self):
        return f"<Price('{self.ticker}')>"
