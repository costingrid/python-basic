"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     # >>> math_calculate('log', 1024, 2)
     # 10.0
     # >>> math_calculate('ceil', 10.7)
     # 11
"""
import math
import pytest


class OperationNotFoundException(Exception):
    def __init__(self):
        self.message = "Operation not found"


def math_calculate(function: str, *args):
    try:
        func = getattr(math, function)
    except AttributeError:
        raise OperationNotFoundException
    return func(*args)


"""
Write tests for math_calculate function
"""


def test_math_calculate():
    assert math_calculate('log', 1024, 2) == 10.0
    assert math_calculate('ceil', 10.7) == 11
    with pytest.raises(OperationNotFoundException):
        math_calculate('log21', 1024, 2)
