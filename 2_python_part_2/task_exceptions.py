"""
Write a function which divides x by y.
If y == 0 it should print "Division by 0" and return None
elif y == 1 it should raise custom Exception with "Deletion on 1 get the same result" text
else it should return the result of division
In all cases it should print "Division finished"
    >>> division(1, 0)
    Division by 0
    Division finished
    >>> division(1, 1)
    Division finished
    DivisionByOneException("Deletion on 1 get the same result")
    >>> division(2, 2)
    1
    Division finished
"""
import typing


class DivisionByOneException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(f"{type(self).__name__}(\"{self}\")")


def division(x: int, y: int) -> typing.Union[None, int]:
    try:
        if y == 0:
            raise ZeroDivisionError("Division by 0")
        elif y == 1:
            raise DivisionByOneException("Deletion on 1 get the same result")
        else:
            print(int(x / y))

    except ZeroDivisionError as ze:
        print(ze)
    # except DivisionByOneException as oe:
    #     print(f"{type(oe).__name__}(\"{oe}\")")
    finally:
        print("Division finished")

    return None
