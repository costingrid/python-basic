"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import os
import pytest
from tempfile import NamedTemporaryFile
from task_read_write import read_write


def test_read_write():
    files_path = os.getcwd()
    with NamedTemporaryFile(mode='w', delete=False, prefix="1-", suffix=".txt", dir=files_path) as file_1:
        file_1.write("23")
    with NamedTemporaryFile(mode='w', delete=False, prefix="2-", suffix=".txt", dir=files_path) as file_2:
        file_2.write("78")
    with NamedTemporaryFile(mode='w', delete=False, prefix="3-", suffix=".txt", dir=files_path) as file_3:
        file_3.write("3")

    read_write(files_path)
    os.remove(file_1.name)
    os.remove(file_2.name)
    os.remove(file_3.name)

    with open(f"{files_path}/output_file", "r") as f:
        assert f.read() == "23, 78, 3"

    os.remove("output_file")


def test_read_write_empty():
    files_path = os.getcwd()
    with NamedTemporaryFile(mode='w', delete=False, prefix="1-", suffix=".txt", dir=files_path) as file_1:
        file_1.write("")

    read_write(files_path)
    os.remove(file_1.name)

    with open(f"{files_path}/output_file", "r") as f:
        assert f.read() == ""

    os.remove("output_file")