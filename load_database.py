import csv
import datetime
import logging
import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import settings as db_settings
from database.helpers import decimal_from_string, InvalidDecimalRecordDataException
from database.models import Base, Ticker, Price

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = 'load_database.log'
TICKER_DOWNLOADS = os.getenv("TICKER_DOWNLOADS")
ECHO = False

logging.basicConfig(
    filename=os.path.join(BASE_DIR, LOG_FILE),
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)


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


def files_with_extension(path, extension):
    return [f for f in os.listdir(path) if f.endswith(extension)]


def date_from_string(date_string):
    dt = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return dt.date()


def prices_from_reader(ticker, reader):
    for row in reader:
        try:
            yield Price(
                ticker_id=ticker.id,
                date=date_from_string(row['Date']),
                open=decimal_from_string(row['Open']),
                high=decimal_from_string(row['High']),
                low=decimal_from_string(row['Low']),
                close=decimal_from_string(row['Close']),
                adj_close=decimal_from_string(row['Adj Close']),
                volume=row['Volume'],
            )
        except InvalidDecimalRecordDataException as e:
            logger.warning(f"Invalid string to decimal conversion for {ticker.ticker} at {row['Date']}.")
            continue
        except Exception as e:
            raise e


def load_database():
    engine = create_engine(db_settings.DB_STRING, echo=ECHO)
    base = Base
    base.metadata.create_all(engine)

    session = get_session(engine=engine)

    csv_extension = '.csv'

    #  Get a list of csv files from the TICKER_DOWNLOADS folder
    csv_files = files_with_extension(TICKER_DOWNLOADS, csv_extension)

    #  For each CSV file create a Ticker object in the database
    symbols = (f.replace(csv_extension, '') for f in csv_files)
    session.add_all([Ticker(ticker=symbol) for symbol in symbols])
    session.commit()

    #  For each CSV file create Price records for every record in the CSV file associated to that files Ticker()
    csv_paths = (os.path.join(TICKER_DOWNLOADS, p) for p in csv_files)
    start_time = time.time()

    for csv_path in csv_paths:
        ticker_str = os.path.split(csv_path)[1].replace(csv_extension, '')
        print(f"Importing price records for '{ticker_str}'.")
        ticker = session.query(Ticker).filter_by(ticker=ticker_str).one()

        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            session.add_all(prices_from_reader(ticker, reader))
            session.commit()

    elapsed_time = time.time() - start_time
    print(f"Total time taken: f{elapsed_time}")


if __name__ == "__main__":
    load_database()
