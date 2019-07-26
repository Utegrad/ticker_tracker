import os
import time

import logging
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MAX_WAIT = 10

logging.basicConfig(
    filename='download.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class WebDriver:
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def content_type(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    return header.get('content-type').lower()


def get_browser_preferences(download_path, save_to_disk_content_types):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_path)
    for ct in save_to_disk_content_types:
        profile.set_preference("browser.helerApps.neverAsk.openFile", ct)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ct)
    return profile


def file_len(fname):
    counter = 0
    with open(fname, 'r') as f:
        for idx, line in enumerate(f):
            counter += 1
    return counter


def history():
    download_dir = os.path.join(BASE_PATH, 'downloads')
    tickers_file = os.path.join(BASE_PATH, 'tickers.txt')
    profile = get_browser_preferences(download_path=download_dir, save_to_disk_content_types=('text/csv',))
    ticker_count = file_len(tickers_file)

    with WebDriver(webdriver.Firefox(firefox_profile=profile)) as driver:
        with open(tickers_file, 'r') as t:
            for idx, line in enumerate(t):
                ticker = line.strip().capitalize()
                percent = 100 * (idx/ticker_count)
                print(f"Getting '{ticker}' - {percent:.2f}%")
                url = f"https://finance.yahoo.com/quote/{ticker}/history?p={ticker}"
                logger.info(f"Getting history for {ticker}")
                try:
                    download(driver, url)
                except Exception as e:
                    print(f"Problem downloading historical data for {ticker}")
                    if hasattr(e, 'message'):
                        logger.warning(e.message)
                    else:
                        logger.warning(e)
                    continue


def download(driver, url):
    logger.info(f"Getting URL: {url}")
    driver.get(url)
    logger.debug(f"Finding input element by xpath")
    time_period_input = driver.find_element_by_xpath("//input[@data-test='date-picker-full-range']")
    logger.debug(f"Clicking date-picker input")
    time_period_input.click()
    logger.debug("Finding 'MAX' span")
    max_time_period = driver.find_element_by_xpath("//span[@data-value='MAX']")
    logger.debug("Clicking 'MAX'")
    max_time_period.click()
    logger.debug("Finding buttons")
    buttons = driver.find_elements_by_tag_name('button')
    logger.debug("Finding 'Done' button")
    done_button = [b for b in buttons if b.text == 'Done'][0]
    logger.debug("Clicking 'Done' button")
    done_button.click()
    logger.debug("Finding download link")
    download_link = driver.find_element_by_xpath("//a[@download]")
    logger.debug("Clicking download link")
    download_link.click()
    logger.debug("Sleep 3 seconds")
    time.sleep(3)


if __name__ == "__main__":
    history()
