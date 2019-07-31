import pytest

from decimal import Decimal

from database import helpers


def test_decimal_from_string_valid_decimal():
    dec_str = '3.147'
    expected_value = Decimal(dec_str)
    result = helpers.decimal_from_string(dec_str)
    assert expected_value == result


def test_decimal_from_string_raises_InvalidRecordDataException():
    test_str = 'null'
    with pytest.raises(helpers.InvalidDecimalRecordDataException):
        result = helpers.decimal_from_string(test_str)
