"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    # >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    # -1
    # >>> calculate_days('2021-10-05')
    # 1
    # >>> calculate_days('10-07-2021')
    # WrongFormatException
"""
from datetime import datetime
from datetime import date
from freezegun import freeze_time
import pytest


class WrongFormatException(Exception):
    def __init__(self):
        self.message = "WrongFormatException"


def calculate_days(from_date: str) -> int:
    today = date.today()
    try:
        date_object = datetime.strptime(from_date, "%Y-%m-%d").date()
    except ValueError:
        raise WrongFormatException
    else:
        return (today - date_object).days


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""


@freeze_time("2021-10-06")
def test_calculate_days_short():
    assert calculate_days('2021-10-02') == 4
    assert calculate_days('2021-10-06') == 0
    assert calculate_days('2021-09-30') == 6


@freeze_time("2021-10-06")
def test_calculate_days_long():
    assert calculate_days('2021-05-02') == 157
    assert calculate_days('2020-10-06') == 365
    assert calculate_days('2019-07-12') == 817


@freeze_time("2021-10-06")
def test_calculate_days_wrong_format():
    with pytest.raises(WrongFormatException):
        calculate_days('2021-10-02-10')
    with pytest.raises(WrongFormatException):
        calculate_days('2021-10-02-10-10')
    with pytest.raises(WrongFormatException):
        calculate_days('10-10-10')


@freeze_time("2021-10-06")
def test_calculate_days_future():
    assert calculate_days('2021-10-07') == -1
    assert calculate_days('2021-10-08') == -2
    assert calculate_days('2021-10-09') == -3
