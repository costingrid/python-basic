import multiprocessing
import os
import time
from random import randint
import concurrent.futures
from os.path import isfile, join
import threading
import shutil

OUTPUT_DIR = './output'
OUTPUT_DIR2 = './output2'
RESULT_FILE = './output/result.csv'
RESULT_FILE2 = './output2/result.csv'


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n - 1):
        f0, f1 = f1, f0 + f1
    return f1


def worker1(n: int):
    value = fib(n)
    with open(f"{OUTPUT_DIR}/{n}.txt", "w") as file:
        file.write(str(value))


def func1(array: list):
    workers = 8 if len(array) > 8 else len(array)
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(worker1, input_arg)
            for input_arg in array
        ]


def func_mea(array: list):
    for num in array:
        value = fib(num)
        with open(f"{OUTPUT_DIR2}/{num}.txt", "w") as file:
            file.write(str(value))


def func_mea2(result_file: str):
    with open(result_file, "w") as file:
        file.write(f"csv file:\n")

    files = [f for f in os.listdir(OUTPUT_DIR2) if isfile(join(OUTPUT_DIR2, f)) and f.split('.')[1] == "txt"]

    for file in files:
        with open(f"{OUTPUT_DIR2}/{file}", "r") as f:
            index = file.split(".")[0]
            value = f.read()
        with open(result_file, "a") as f:
            f.write(f"{index}, {value}\n")


def worker2(result_file: str, file: str, lock: multiprocessing.Lock):
    with open(f"{OUTPUT_DIR}/{file}", "r") as f:
        index = file.split('.')[0]
        value = f.read()

    with lock:
        with open(result_file, 'a+') as file:
            file.write(f"{index}, {value}\n")


def func2(result_file: str):
    with open(result_file, "w") as file:
        file.write("csv file:\n")

    files = [f for f in os.listdir(OUTPUT_DIR) if isfile(join(OUTPUT_DIR, f)) and f.split('.')[1] == "txt"]

    lock = threading.Lock()

    workers = 8 if len(files) > 8 else len(files)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(worker2, result_file, filename, lock)
            for filename in files
        ]

    pass

# rulez o data secvential si o data in paralel si afisez durata
if __name__ == '__main__':

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    if os.path.exists(OUTPUT_DIR2):
        shutil.rmtree(OUTPUT_DIR2)

    os.makedirs(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR2)

    arr = [randint(1000, 10000) for _ in range(10000)]

    start = time.time()
    func_mea(arr)
    duration = time.time() - start
    print(duration)

    start = time.time()
    func1(array=arr)
    duration = time.time() - start
    print(duration)

    start = time.time()
    func_mea2(result_file=RESULT_FILE2)
    duration = time.time() - start
    print(duration)

    start = time.time()
    func2(result_file=RESULT_FILE)
    duration = time.time() - start
    print(duration)
