import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Ticker, Price
from database import settings as db_settings

TICKER_DOWNLOADS = os.getenv("TICKER_DOWNLOADS")


def load_database():
    engine = create_engine(db_settings.DB_STRING, echo=True)
    base = Base
    base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    a_ticker = Ticker(ticker="A")
    session.add(a_ticker)

    the_ticker = session.query(Ticker).filter_by(ticker='A').first()
    print(the_ticker)
    session.commit()


if __name__ == "__main__":
    load_database()
