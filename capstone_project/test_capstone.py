import pytest
import subprocess
import os
import json
import shutil

@pytest.fixture
def temp_dir():
    dir_path = os.getcwd() + "/temp"
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    yield dir_path


def test_full_run(temp_dir):
    file_count = 2
    file_name = "test_data"
    prefix = "count"
    data_schema = '{"name": "str:rand", "age": "int:rand(0,100)"}'
    data_lines = 5
    command = [
        "python3", "capstone.py",
        str(temp_dir),
        "--file_count", str(file_count),
        "--file_name", file_name,
        "--prefix", prefix,
        "--data_schema", data_schema,
        "--data_lines", str(data_lines)
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0

    for i in range(2):
        file_path = f"{temp_dir}/{i}_test_data.json"
        assert os.path.exists(file_path)

        with open(file_path, 'r') as file:
            data = json.load(file)
            assert len(data) == data_lines
            assert "name" in data[0] and all(len(data[i]["name"]) == 36 for i in range(len(data)))
            assert "age" in data[0] and all(0 <= data[i]["age"] <= 100 for i in range(len(data)))


def test_bad_data_schema(temp_dir):
    file_count = 2
    file_name = "test_data"
    prefix = "count"
    data_schema = '{"name": "str:rand(0,100)", "age": "int:rand(0,100)"}'
    data_lines = 5
    command = [
        "python3", "capstone.py",
        str(temp_dir),
        "--file_count", str(file_count),
        "--file_name", file_name,
        "--prefix", prefix,
        "--data_schema", data_schema,
        "--data_lines", str(data_lines)
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Bad format for random string" in result.stderr


def test_file_count_zero():
    file_count = 0
    file_name = "test_data"
    prefix = "count"
    data_schema = '{"name": "str:rand", "age": "int:rand(0,100)"}'
    data_lines = 5
    command = [
        "python3", "capstone.py",
        '.',
        "--file_count", str(file_count),
        "--file_name", file_name,
        "--prefix", prefix,
        "--data_schema", data_schema,
        "--data_lines", str(data_lines)
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    with open("output", 'w') as file:
        output = output.split('\n')[:-1]
        output = '\n'.join(output)
        file.write(output)
    with open("output", 'r') as file:
        output = json.load(file)
    os.remove("output")

    assert result.returncode == 0
    assert len(output) == data_lines
    assert "name" in output[0] and all(len(output[i]["name"]) == 36 for i in range(len(output)))
    assert "age" in output[0] and all(0 <= output[i]["age"] <= 100 for i in range(len(output)))


def test_data_scheme_path(temp_dir):
    file_count = 2
    file_name = "test_data"
    prefix = "count"
    data_schema = "temp/data_schema.json"
    data_lines = 5
    with open(f"{temp_dir}/data_schema.json", 'w') as file:
        json.dump({"name": "str:rand", "age": "int:rand(0,100)"}, file)

    command = [
        "python3", "capstone.py",
        str(temp_dir),
        "--file_count", str(file_count),
        "--file_name", file_name,
        "--prefix", prefix,
        "--data_schema", data_schema,
        "--data_lines", str(data_lines)
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0

    for i in range(2):
        file_path = f"{temp_dir}/{i}_test_data.json"
        assert os.path.exists(file_path)

        with open(file_path, 'r') as file:
            data = json.load(file)
            assert len(data) == data_lines
            assert "name" in data[0] and all(len(data[i]["name"]) == 36 for i in range(len(data)))
            assert "age" in data[0] and all(0 <= data[i]["age"] <= 100 for i in range(len(data)))
