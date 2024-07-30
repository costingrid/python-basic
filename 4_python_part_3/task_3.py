"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    # >>> is_http_domain('http://wikipedia.org')
    # True
    # >>> is_http_domain('https://ru.wikipedia.org/')
    # True
    # >>> is_http_domain('griddynamics.com')
    # False
"""
import re
import pytest


def is_http_domain(domain: str) -> bool:
    format = r'https?:\/\/[a-zA-Z.1-9]+\/?$'
    regex = re.compile(format)
    return regex.match(domain) is not None


"""
write tests for is_http_domain function
"""


def test_is_http_domain():
    assert is_http_domain('http://w')
    assert is_http_domain('https://wikipedia.org')
    assert is_http_domain('http://wikipedia.org')
    assert is_http_domain('https://ru.wikipedia.org/')


def test_is_not_http_domain():
    assert not is_http_domain('griddynamics.com')
    assert not is_http_domain('httpss://ru.wikipedia.org')
    assert not is_http_domain('htp://wikipedia.org/')
    assert not is_http_domain('https://ru.wikipedia.org//')