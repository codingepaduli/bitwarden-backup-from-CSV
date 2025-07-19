from argparse import ArgumentParser
from pathlib import Path
import sys
import csv
from config import initLogger
from os import strerror
import errno
import logging

def get_folder(element: dict[str, str]) -> str:
    return element['folder']

def loadCSV(filename: Path) -> tuple[list[dict[str,str]], Exception | None]:
    """
    Load the CSV file as a list of dictionaries. Each row is a dictionary.

    Parameters
    ----------
    filename: Path
        The CSV file to load
    
    Returns
    -------
    tuple[list[dict[str,str]], Exception | None]: 
        list[dict[str,str]:
            is a list of rows. Each row is a dictionary.
        Exception | None: 
            FileNotFoundError if the folder is None or is not a valid directory 
            None in case of success (no error happens)
    """

    logger: logging.Logger = logging.getLogger(__name__)

    fileRows : list[dict[str,str]] = []
    error: Exception | None = None

    logger.info(f"loading file {filename}")

    if filename is None or not filename.is_file():
        error = FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), filename)
        logger.error(f"file doesn't exists: {filename}")
        return fileRows, error
    
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        try:
            row : dict[str, str]
            for row in reader:
                fileRows.append(row)
            
            logger.info(f"Loaded {len(fileRows)} rows from file {filename}")
        except csv.Error as e:
            logger.error('file {}, line {}: {}'.format(csvfile, reader.line_num, e))
            fileRows = []
            error = e

    return fileRows, error

if __name__ == "__main__":
    """
    Load a CSV file and make a printable text for each row.
    
    The columns to print are chosen from the command line option --columns. 
    The first column is the column 1. An empty --columns option will 
    chose all the fields.
    """
    arg_parser = ArgumentParser(prog='makePrintableListFromCSV', allow_abbrev=False, description="Load the bitwarden backup CSV file and make a printable list of each row")
    arg_parser.add_argument(
        "-i",                # short parameter name
        "--input-file",      # long parameter name
        type=Path,           # argument type
        required=True,
        action="store",      # store the value in memory
        metavar='input_file', # displayed name (in help messages)
        help="The CSV file to load."
    )
    
    parsed_args = arg_parser.parse_args()
    
    initLogger()
    
    logger : logging.Logger = logging.getLogger(__name__)
    
    fileRows : list[dict[str,str]] = []
    error : Exception | None = None

    fileRows, error = loadCSV(parsed_args.input_file)

    if error is not None:
        logger.error(f"Error loading the CSV file: {error}")
        sys.exit(1)
    
    # sort by folder
    fileRows.sort(key=get_folder)

    # Current CSV header
    # folder, type, name, notes, fields, reprompt, 
    # login_uri, login_username, login_password, login_totp

    print("# My Vault\n")

    print("## Notes\n")

    for row in fileRows:
        if row['type'] == 'note':
            print(f"### {row['folder']} - {row['name']}\n")
            print(f"{row['notes']} - {row['fields']} -\n")

    print("## Credentials\n")

    for row in fileRows:
        if row['type'] == 'login':
            print(f"### {row['folder']} - {row['name']}\n")
            print(f"{row['login_username']} - {row['login_password']} - {row['notes']} -\n") 
            print(f"{row['login_uri']}\n")
