import requests
from selenium import webdriver


class WebDriver:
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text/csv' in content_type.lower():
        return True
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def content_type(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    return header.get('content-type').lower()


def history():
    with WebDriver(webdriver.Firefox()) as driver:
        driver.get("https://finance.yahoo.com/quote/BX/history?p=BX")
        time_period_input = driver.find_element_by_xpath("//input[@data-test='date-picker-full-range']")
        time_period_input.click()
        max_time_period = driver.find_element_by_xpath("//span[@data-value='MAX']")
        max_time_period.click()
        buttons = driver.find_elements_by_tag_name('button')
        done_button = [b for b in buttons if b.text == 'Done'][0]
        done_button.click()
        download_link = driver.find_element_by_xpath("//a[@download]")
        download_url = download_link.get_attribute("href")
        if is_downloadable(download_url):
            with requests.get(download_url, stream=True, allow_redirects=True) as r:
                r.raise_for_status()
                with open('BX.txt', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        else:
            print(f"{download_url} - ({content_type(download_url)}) is not is not downloadable")


if __name__ == "__main__":
    history()
