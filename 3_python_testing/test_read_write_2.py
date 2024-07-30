"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import os
import pytest
from tempfile import NamedTemporaryFile
from task_read_write_2 import read_write_2
# import magic


def test_read_write_2_content():
    files_path = os.getcwd()

    words = read_write_2(files_path)

    with open(f"{files_path}/file1.txt", "r") as file1, open(f"{files_path}/file2.txt", "r") as file2:
        assert file1.read() == "\n".join(words) and file2.read() == ", ".join(reversed(words))

    os.remove(f"{files_path}/file1.txt")
    os.remove(f"{files_path}/file2.txt")


''' nu merge python-magic'''
# def test_read_write_2_encoding():
#     files_path = os.getcwd()
#
#     read_write_2(files_path)
#     blob1 = open(f"{files_path}/file1.txt", 'rb').read()
#     m = magic.open(magic.MAGIC_MIME_ENCODING)
#     m.load()
#     encoding1 = m.buffer(blob1)
#
#     blob2 = open(f"{files_path}/file2.txt", 'rb').read()
#     m = magic.open(magic.MAGIC_MIME_ENCODING)
#     m.load()
#     encoding2 = m.buffer(blob2)
#     assert encoding1 == "utf-8" and encoding2 == "Windows-1252"
#
#     os.remove(f"{files_path}/file1.txt")
#     os.remove(f"{files_path}/file2.txt")
