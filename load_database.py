import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Ticker, Price
from database import settings as db_settings

TICKER_DOWNLOADS = os.getenv("TICKER_DOWNLOADS")


def get_session(engine=None, echo=None):
    """ Return a sqlalchemy Session()

    :param engine:  Defaults to creating a new session if engine is None
    :param echo: Defaults to False, used to set echo parameter if creating an engine
    :return: sqlalchemy session
    """

    echo = False if echo is None else echo

    if engine is None:
        engine = create_engine(db_settings.DB_STRING, echo=echo)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def load_database():

    engine = create_engine(db_settings.DB_STRING, echo=True)
    base = Base
    base.metadata.create_all(engine)

    session = get_session(engine=engine)

    #  Get a list of csv files from the TICKER_DOWNLOADS folder
    #  For each CSV file create a Ticker object in the database
    #  For each CSV file create Price records for every record in the CSV file associated to that files Ticker()


if __name__ == "__main__":
    load_database()
