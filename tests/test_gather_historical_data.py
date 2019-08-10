""" Tests for the gather_historical_data module

"""
import os
import tempfile

from gather_historical_data import tickers

tickers_file_content = """A
AA
AAC
AAN
AAP
"""


def test_tickers_text():
    handle, path = tempfile.mkstemp()
    try:
        with os.fdopen(handle, 'w') as tmp:
            tmp.write(tickers_file_content)
        ts = tickers(path)
        assert any([t for t in list(ts) if t == "AAN"])
    finally:
        os.remove(path)
