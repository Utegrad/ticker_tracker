from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ticker(Base):
    __tablename__ = 'tickers'
    id = Column(Integer, primary_key=True, )
    name = Column(String(length=64, ), nullable=True, )
    ticker = Column(String(length=8, ), nullable=False, index=True, unique=True, )


class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True, )
    ticker_id = Column(Integer, ForeignKey('tickers.id'), nullable=False)
    date = Column(Date, nullable=False, )
    open = Column(DECIMAL, nullable=False)
    high = Column(DECIMAL, nullable=False)
    low = Column(DECIMAL, nullable=False)
    close = Column(DECIMAL, nullable=False)
    adj_close = Column(DECIMAL, nullable=False)
    volume = Column(Integer, nullable=False)
