import argparse
import concurrent.futures
import configparser
import json
import logging
import os
import random
import shutil
import sys
import time
import uuid
from colorama import init, Fore

init()


class TextFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.ERROR:
            color = Fore.RED
        else:
            color = Fore.WHITE
        message = super().format(record)
        return f"{color}{message}{Fore.RESET}"


handler = logging.StreamHandler()
handler.setFormatter(TextFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[handler])
logging.getLogger().setLevel(logging.INFO)


def validate_path(path):
    logging.info(f"Validating path: {path}")
    if not os.path.exists(path):
        logging.error(f"Error: {path} does not exist.")
        sys.exit(1)
    elif not os.path.isdir(path):
        logging.error(f"Error: {path} is not a directory.")
        sys.exit(1)


def validate_multiprocessing(mp):
    logging.info(f"Validating number of processes: {mp}")
    if mp < 0:
        logging.error(f"Error: Number of processes must be greater than 0.")
        sys.exit(1)
    return min(mp, os.cpu_count())


def load_schema(schema):
    logging.info(f"Loading schema: {schema}")
    try:
        if os.path.exists(schema):
            with open(schema, 'r') as file:
                return json.load(file)
        else:
            return json.loads(schema)
    except (json.JSONDecodeError, OSError) as e:
        logging.error(f"Error loading schema: {e}")
        sys.exit(1)


def generate_data(schema, data_lines):
    data = [{} for _ in range(data_lines)]

    for key in schema:
        value = schema[key]
        if str.startswith(value, 'timestamp'):
            for i in range(data_lines):
                data[i][key] = str(time.time())
        elif str.startswith(value, 'str'):
            option = value.split(':')[1]
            if option == 'rand':
                for i in range(data_lines):
                    data[i][key] = str(uuid.uuid4())
            elif str.startswith(option, 'rand('):
                logging.error(f"Bad format for random string")
                sys.exit(1)
            elif str.startswith(option, '['):
                options = option[1:-1].split(', ')
                if all(option[0] == option[-1] == '\'' or option[0] == option[-1] == '\"' for option in options):
                    for i in range(data_lines):
                        data[i][key] = str(random.choice(options)).strip('\'')
                else:
                    logging.error(f"Bad format for string {value}")
                    sys.exit(1)
            elif len(value) > 0:
                value = value.split(':')[1]
                for i in range(data_lines):
                    data[i][key] = str(value)
            else:
                for i in range(data_lines):
                    data[i][key] = ''
        elif str.startswith(value, 'int'):
            option = value.split(':')[1]
            if option == 'rand':
                for i in range(data_lines):
                    data[i][key] = random.randint(0, 10000)
            elif str.startswith(option, 'rand('):
                options = option[5:-1].split(',')
                for i in range(data_lines):
                    data[i][key] = random.randint(int(options[0]), int(options[1]))
            elif str.startswith(option, '['):
                options = option[1:-1].split(',')
                for i in range(data_lines):
                    data[i][key] = int(random.choice(options))
            elif len(value) > 0:
                for i in range(data_lines):
                    try:
                        data[i][key] = int(value)
                    except ValueError:
                        logging.error(f"Bad format for integer {value}")
                        sys.exit(1)
            else:
                for i in range(data_lines):
                    data[i][key] = None

    return data


def worker(file_path, schema, data_lines):
    try:
        with open(file_path, 'w') as file:
            data = generate_data(schema, data_lines)
            json.dump(data, file, indent=4)
    except OSError as e:
        logging.error(f"Error writing to file {file_path}: {e}")


def main():
    config = configparser.ConfigParser()
    config.read('default.ini')

    parser = argparse.ArgumentParser(description='Generate JSON files with random data')
    parser.add_argument('path_to_save_files', help='Path to save files')
    parser.add_argument('--file_count', type=int, default=config.getint('DEFAULT', 'file_count', fallback=1),
                        help='Number of JSON files to generate')
    parser.add_argument('--file_name', default=config.get('DEFAULT', 'file_name', fallback='data'),
                        help='Base file name')
    parser.add_argument('--prefix', choices=['count', 'random', 'uuid'],
                        default=config.get('DEFAULT', 'prefix', fallback='count'), help='Prefix for file name')
    parser.add_argument('--data_schema', default=config.get('DEFAULT', 'data_schema', fallback='{}'),
                        help='JSON schema as a string or path to a JSON file')
    parser.add_argument('--data_lines', type=int, default=config.getint('DEFAULT', 'data_lines', fallback=1000),
                        help='Number of lines per file')
    parser.add_argument('--clear_path', action='store_true',
                        default=config.getboolean('DEFAULT', 'clear_path', fallback=False),
                        help='Clear path before creating new files')
    parser.add_argument('--multiprocessing', type=int, default=config.getint('DEFAULT', 'multiprocessing', fallback=1),
                        help='Number of processes to use')

    args = parser.parse_args()

    if args.clear_path and os.path.exists(args.path_to_save_files):
        try:
            shutil.rmtree(args.path_to_save_files)
        except OSError as e:
            logging.error(f"Error clearing path {args.path_to_save_files}: {e}")
            sys.exit(1)
    if not args.file_count==0:
        validate_path(args.path_to_save_files)
    cpus = validate_multiprocessing(args.multiprocessing)
    schema = load_schema(args.data_schema)
    if args.file_count > 0:
        logging.info(f"Started generating data.")
        if args.prefix == 'count':
            with concurrent.futures.ProcessPoolExecutor(max_workers=cpus) as executor:
                futures = [
                    executor.submit(worker, os.path.join(args.path_to_save_files,
                                    f"{i}_{args.file_name}.json"),
                                    schema, args.data_lines)
                    for i in range(args.file_count)
                ]
                for future in concurrent.futures.as_completed(futures):
                    if future.exception() is not None:
                        logging.error(f"Error in worker: {future.exception()}")
        elif args.prefix == 'random':
            with concurrent.futures.ProcessPoolExecutor(max_workers=cpus) as executor:
                futures = [
                    executor.submit(worker, os.path.join(args.path_to_save_files,
                                    f"{random.randint(1, 10000)}_{args.file_name}.json"),
                                    schema, args.data_lines)
                    for _ in range(args.file_count)
                ]
                for future in concurrent.futures.as_completed(futures):
                    if future.exception() is not None:
                        logging.error(f"Error in worker: {future.exception()}")
        elif args.prefix == 'uuid':
            with concurrent.futures.ProcessPoolExecutor(max_workers=cpus) as executor:
                futures = [
                    executor.submit(worker, os.path.join(args.path_to_save_files,
                                    f"{str(uuid.uuid4())}_{args.file_name}.json"),
                                    schema, args.data_lines)
                    for _ in range(args.file_count)
                ]
                for future in concurrent.futures.as_completed(futures):
                    if future.exception() is not None:
                        logging.error(f"Error in worker: {future.exception()}")
        logging.info(f"Finished generating data.")
    else:
        logging.info(f"Started generating data.")
        data = generate_data(schema, args.data_lines)
        print(json.dumps(data, indent=4))
        logging.info(f"Finished generating data.")


if __name__ == '__main__':
    main()

