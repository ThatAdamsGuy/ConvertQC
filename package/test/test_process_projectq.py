import sys
import os
import unittest
import argparse
from unittest import mock

sys.path.insert(0, '../convertqc')
from convertqc import process_projectq

output_file = None
args = None

print("RUNNING TESTS - process_projectq.py")


def process_args():
    """
    Creates the ArgumentParser to handle input arguments.
    Future arguments are easily added with a new .add_argument() line
    :return: None
    """

    global args
    parser = argparse.ArgumentParser(
        description="Convert quantum circuits into different environments")

    # Optional - user defined output name
    parser.add_argument(
        "-o",
        "--output_filename",
        help="set output filename, without file extension (default: convertqc_result.<filetype>")
    # Optional - verbose mode
    parser.add_argument(
        "-v",
        "--verbose",
        help="run in verbose mode",
        action="store_true")
    # Optional - remove code comments identifying untranslated lines
    parser.add_argument(
        "-m",
        "--mark",
        help="disable comments in code to identify untranslated lines",
        action="store_false")
    # Optional - disable output of error log
    parser.add_argument(
        "-e",
        "--error_log",
        help="disable outputting error log to file",
        action="store_false")
    # Optional - debug mode
    parser.add_argument(
        "-d",
        "--debug",
        help="enable debug mode",
        action="store_true")

    args = parser.parse_args()

    if args.debug:
        args.verbose = True


class ConvertGateTests(unittest.TestCase):
    def testPauliXGate(self):
        global output_file
        process_args()
        output_file = open("test_output.txt", "w+")

        line = "X | Qubit"
        process_projectq.convert_gate(line)


