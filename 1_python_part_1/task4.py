"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]
    >>> # because [1^2, 2^2 - (1^2 - 1), 3^2 - (2^2 - 2)]
"""
from typing import List


# presupun ca power se refera doar la patrat
def calculate_power_with_difference(ints: List[int]) -> List[int]:
    result = list()
    previous_value = 0
    calc = lambda a, b: a ** 2 - (b ** 2 - b)
    for i in range(len(ints)):
        result.append(calc(ints[i], previous_value))
        previous_value = ints[i]

    return result
