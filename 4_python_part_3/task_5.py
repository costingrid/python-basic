"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     # >>> make_request('https://www.google.com')
     # 200, 'response data'
"""
import urllib.error
from typing import Tuple
from urllib.request import urlopen
from unittest.mock import Mock, patch


def make_request(url: str) -> Tuple[int, str]:
    try:
        page = urlopen(url)
        response = page.read().decode("ISO-8859-1").encode("utf-8").decode("utf-8")
        code = page.code
        return code, response
    except urllib.error.HTTPError as e:
        response = e.read().decode()
        return e.code, response
    except urllib.error.URLError as e:
        return 404, str(e)


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""


def test_make_request():
    m = Mock()
    m.code = 200
    m.read.return_value = b'some text'
    m.decode.return_value = 'some text'
    with patch('urllib.request.urlopen', return_value=m):
        code, response = make_request('https://www.google.com')
        assert code == 200
        assert 'http://schema.org/WebPage' in response
        assert len(response) > 0


def test_make_request_bad_url():
    m = Mock()
    m.code = 404
    m.read.return_value = b'Not Found'
    m.decode.return_value = 'Not Found'
    with patch('urllib.request.urlopen', return_value=m):
        code, response = make_request('https://www.gloogle.com')
        assert code == 404
        assert 'Not Found' in response
        assert len(response) > 0
