import pytest

from helpers import has_punctuation

has_punctuation_test_values = [
    ("ABC", False),
    ("AB-C", True),
    ("AB.C", True),
    ("AB_C", True),
]


@pytest.mark.parametrize("value, expected", has_punctuation_test_values)
def test_has_punctuation(value, expected):
    assert has_punctuation(value) is expected
