import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database import settings as db_settings
from database.models import Base, Ticker, Price

engine = create_engine(db_settings.DB_STRING, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    prices = session.query(Price)[:20]
    df = pd.DataFrame(prices)
    print(df)
