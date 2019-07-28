import os
import string
import time

import requests
from selenium.common.exceptions import WebDriverException


def ls_l(path):
    """ yield the full path to directory listing of path

    :param path: path to get directory listing of
    :return: generator of full paths from directory listing of path
    """
    for f in os.listdir(path):
        yield os.path.join(path, f)


def wait(fn, max_wait=10):
    """ Wait on a selenium get element method for max_wait time

    :param fn: function to wait on
    :param max_wait: seconds to wait for WebDriverException errors to clear
    :return: return value of fn
    """

    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > max_wait:
                    raise e
                time.sleep(0.5)

    return modified_fn


def content_type(url):
    """ Get the 'content-type' header from a url """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    return header.get("content-type").lower()


def file_len(fname):
    """ Get the number of lines from a filename

    :param fname: file name to get number of lines from
    :return: integer for the number of lines in the given fname
    """
    counter = 0
    with open(fname, "r") as f:
        for idx, line in enumerate(f):
            counter += 1
    return counter


def has_punctuation(s) -> bool:
    """ Check if a given string has punctuation in it

    :param s: a string to test for punctuation
    :return: boolean True is punctuation is present, otherwise false
    """
    present = False
    for char in string.punctuation:
        if char in s:
            return True
    return present
