"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""
import glob
import os
import re


# class ReadWrite:
#     def __init__(self, files_path):
#         self.files_path = files_path
#         self.first = True
#         self.numbers = re.compile(r'(\d+)')
#
#     def read_write(self):
#         def numerical_sort(value):
#             parts = self.numbers.split(value)
#             parts[1::2] = map(int, parts[1::2])
#             return parts
#
#         with open("output_file", "w") as output:
#             for file in sorted(glob.glob(os.path.join(self.files_path, "*.txt")), key=numerical_sort):
#                 with open(os.path.join(os.getcwd(), file), "r") as f:
#                     if self.first:
#                         output.write(f.readline())
#                         self.first = False
#                     else:
#                         output.write(" , " + f.readline())


def read_write(files_path: str):
    first = True
    numbers = re.compile(r'(\d+)')

    def numerical_sort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    with open(f"{files_path}/output_file", "w") as output:
        for file in sorted(glob.glob(os.path.join(files_path, "*.txt")), key=numerical_sort):
            with open(os.path.join(os.getcwd(), file), "r") as f:
                if first:
                    output.write(f.readline())
                    first = False
                else:
                    output.write(", " + f.readline())
