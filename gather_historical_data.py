""" Download historical data for tickers in TICKERS_FILE from Yahoo and save it in DOWNLOAD_DIR
    Use a Selenium WebDriver to download historical stock price data from Yahoo
"""
import os
import time

import logging
from selenium import webdriver

from helpers import file_len

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MAX_WAIT = 10
DOWNLOAD_DIR = "downloads"
TICKERS_FILE = "filtered_tickers.txt"

logging.basicConfig(
    filename="download.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


class WebDriver:
    """ Context manager for a given WebDriver """

    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def browser_preferences(download_path, save_to_disk_content_types):
    """ Create a FirefoxProfile to control download and save to disk content behaviors in the browser

    :param download_path: Where to save files set to always download
    :param save_to_disk_content_types: list of content-type values to always save to disk
    :return: FirefoxProfile()
    """
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    logger.debug(f"Setting download path to '{download_path}'")
    profile.set_preference("browser.download.dir", download_path)
    for ct in save_to_disk_content_types:
        profile.set_preference("browser.helerApps.neverAsk.openFile", ct)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ct)
    return profile


def download_history_files(tickers_file):
    """ Download historical data for tickers in TICKERS_FILE from Yahoo and save it in DOWNLOAD_DIR

    Use a Selenium WebDriver to download historical stock price data from Yahoo
    :return: None
    """
    download_dir = os.path.join(BASE_PATH, DOWNLOAD_DIR)
    tickers_file = os.path.join(BASE_PATH, tickers_file)
    profile = browser_preferences(
        download_path=download_dir, save_to_disk_content_types=("text/csv",)
    )
    ticker_count = file_len(tickers_file)

    with WebDriver(webdriver.Firefox(firefox_profile=profile)) as driver:
        driver.maximize_window()
        with open(tickers_file, "r") as t:
            for idx, line in enumerate(t):
                ticker = line.strip().capitalize()
                percent = 100 * (idx / ticker_count)
                print(f"Getting '{ticker}' - {percent:.2f}%")
                url = f"https://finance.yahoo.com/quote/{ticker}/history?p={ticker}"
                logger.info(f"Getting history for {ticker}")
                try:
                    download(driver, url)
                except Exception as e:
                    print(f"Problem downloading historical data for {ticker}")
                    if hasattr(e, "message"):
                        logger.warning(e.message)
                    else:
                        logger.warning(e)
                    continue


def download(driver, url, post_download_sleep=2):
    """ Given a WebDriver and a url get and click the download historical data link

    :param driver: WebDriver instance to drive
    :param url: URL for a ticker
    :param post_download_sleep: seconds for the process to sleep after clicking download.
        Done to avoid moving to the next URL too fast and getting stuck.

    :return: None
    """
    logger.info(f"Getting URL: {url}")
    driver.get(url)
    logger.debug(f"Finding input element by xpath")
    time_period_input = driver.find_element_by_xpath(
        "//input[@data-test='date-picker-full-range']"
    )
    logger.debug(f"Clicking date-picker input")
    time_period_input.click()
    logger.debug("Finding 'MAX' span")
    max_time_period = driver.find_element_by_xpath("//span[@data-value='MAX']")
    logger.debug("Clicking 'MAX'")
    max_time_period.click()
    logger.debug("Finding buttons")
    buttons = driver.find_elements_by_tag_name("button")
    logger.debug("Finding 'Done' button")
    done_button = [b for b in buttons if b.text == "Done"][0]
    logger.debug("Clicking 'Done' button")
    done_button.click()
    logger.debug("Finding download link")
    download_link = driver.find_element_by_xpath("//a[@download]")
    logger.debug("Clicking download link")
    download_link.click()
    logger.debug(f"Sleep {post_download_sleep} seconds")
    time.sleep(post_download_sleep)


if __name__ == "__main__":
    download_history_files(tickers_file=TICKERS_FILE)
