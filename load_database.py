import concurrent.futures
import csv
import datetime
import logging
import os
import threading
import time
import itertools

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database import settings as db_settings
from database.helpers import decimal_from_string, InvalidDecimalRecordDataException
from database.models import Base, Ticker, Price

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = "load_database.log"
TICKER_DOWNLOADS = os.getenv("TICKER_DOWNLOADS")
ECHO = False
WORKERS = 5

logging.basicConfig(
    filename=os.path.join(BASE_DIR, LOG_FILE),
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)
csv_extension = ".csv"
engine = create_engine(db_settings.DB_STRING, echo=ECHO)
base = Base
base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def files_with_extension(path, extension):
    return [f for f in os.listdir(path) if f.endswith(extension)]


def date_from_string(date_string):
    dt = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return dt.date()


def prices_from_reader(ticker, reader):
    for row in reader:
        try:
            yield Price(
                ticker_id=ticker.id,
                date=date_from_string(row["Date"]),
                open=decimal_from_string(row["Open"]),
                high=decimal_from_string(row["High"]),
                low=decimal_from_string(row["Low"]),
                close=decimal_from_string(row["Close"]),
                adj_close=decimal_from_string(row["Adj Close"]),
                volume=row["Volume"],
            )
        except InvalidDecimalRecordDataException:
            logger.warning(
                f"Invalid string to decimal conversion for {ticker.ticker} at {row['Date']}."
            )
            continue
        except Exception as e:
            raise e


def get_thread(fn, **kwargs):
    return threading.Thread(
        target=fn,
        kwargs={
            "engine": kwargs['engine'],
            "csv_extension": kwargs['file_extension'],
            "csv_path": kwargs['csv_path'],
        },
    )


def load_database():
    #  Get a list of csv files from the TICKER_DOWNLOADS folder
    csv_files = files_with_extension(TICKER_DOWNLOADS, csv_extension)

    #  For each CSV file create a Ticker object in the database
    symbols = (f.replace(csv_extension, "") for f in csv_files)
    session = Session()
    session.add_all([Ticker(ticker=symbol) for symbol in symbols])
    session.commit()

    #  For each CSV file create Price records for every record in the CSV file associated to that files Ticker()
    csv_paths = (os.path.join(TICKER_DOWNLOADS, p) for p in csv_files)
    try:
        start_time = time.time()

        engine_data = itertools.zip_longest([], list(csv_paths)[:20], fillvalue=engine)
        with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
            executor.map(load_ticker_wrapper, engine_data)

        elapsed_time = time.time() - start_time
        print(f"Total time taken: f{elapsed_time}")
    except Exception as e:
        logger.exception(msg="Error inserting prices for tickers.")
        raise e
    finally:
        Session.remove()


def load_ticker_wrapper(engine_data):
    load_ticker(csv_path=engine_data[1])


def load_ticker(csv_path):
    ticker_str = os.path.split(csv_path)[1].replace(csv_extension, "")
    print(f"Importing price records for '{ticker_str}'.")
    session = Session()
    ticker = session.query(Ticker).filter_by(ticker=ticker_str).one()
    logger.debug(f"{ticker} from database for {ticker_str}")
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        session.add_all(prices_from_reader(ticker, reader))
    session.commit()


if __name__ == "__main__":
    load_database()
