import datetime

from load_database import date_from_string


def test_date_from_string():
    #  Given date string '1996-05-13'
    date_string = '1996-05-13'
    expected_date = datetime.date(1996, 5, 13)
    result = date_from_string(date_string)
    assert result == expected_date
