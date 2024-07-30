"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import sys
from unittest.mock import Mock
import faker
import unittest


def print_name_address(args: argparse.Namespace) -> None:
    arguments = vars(args)
    # print(arguments, file=open('output.txt', 'w'))
    with open('output.txt', 'w') as f:
        f.close()
    fake = faker.Faker()
    for _ in range(arguments['number']):
        entry = {}
        with open('output.txt', 'a') as f:
            for i in arguments['fields']:
                arg_name, arg_type = i.split('=')
                key = arg_name
                if "name" in arg_type:
                    entry[key] = fake.name()
                elif "address" in arg_type:
                    entry[key] = fake.address()
            f.write(str(entry) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    parser.add_argument('number', type=int)
    parser.add_argument('--fields', type=str, nargs='+')
    args = parser.parse_args()
    print_name_address(args)

"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""


class TestPrintNameAddress(unittest.TestCase):

    def test_print_name_address(self):
        m = Mock()
        m.number = 2
        m.fields = ['some_name=name', 'fake_address=address']
        print_name_address(m)

        with open('output.txt', 'r') as f:
            result = f.readlines()
            self.assertEqual(len(result), m.number)
            self.assertTrue('some_name' in result[0])
            self.assertTrue('fake_address' in result[0])
            self.assertTrue('some_name' in result[1])
            self.assertTrue('fake_address' in result[1])

    def test_print_name_address_no_address(self):
        m = Mock()
        m.number = 2
        m.fields = ['some_name=name']
        print_name_address(m)

        with open('output.txt', 'r') as f:
            result = f.readlines()
            self.assertEqual(len(result), m.number)
            self.assertTrue('some_name' in result[0])
            self.assertTrue('fake_address' not in result[0])
            self.assertTrue('some_name' in result[1])
            self.assertTrue('fake_address' not in result[1])

    def test_print_name_address_no_name(self):
        m = Mock()
        m.number = 2
        m.fields = ['fake_address=address']
        print_name_address(m)

        with open('output.txt', 'r') as f:
            result = f.readlines()
            self.assertEqual(len(result), m.number)
            self.assertTrue('some_name' not in result[0])
            self.assertTrue('fake_address' in result[0])
            self.assertTrue('some_name' not in result[1])
            self.assertTrue('fake_address' in result[1])

    def test_print_name_address_no_name_no_address(self):
        m = Mock()
        m.number = 2
        m.fields = []
        print_name_address(m)

        with open('output.txt', 'r') as f:
            result = f.readlines()
            self.assertEqual(len(result), m.number)
            self.assertTrue('some_name' not in result[0])
            self.assertTrue('fake_address' not in result[0])
            self.assertTrue('some_name' not in result[1])
            self.assertTrue('fake_address' not in result[1])
