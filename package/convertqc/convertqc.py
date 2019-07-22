#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

#    Entry point for ConvertQC. Run "convertqc -h" for details.
#    Copyright (C) 2019  Harry Adams (convertqc@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>

import argparse   # Processing arguments
import argcomplete
import os         # Check for input file existing
from . import process_projectq, error_cqc, process_qutip, conversion, process_qiskit

# List of possible input and output formats

valid_program_types = [
    'projectq',
    'qutip',
    'qiskit'
]

filename = ""
args = None


def main():
    """
    Entry point for ConvertQC
    :return: None
    """

    process_args()
    if args.input_format == args.output_format:
        error_cqc.process_error(error_cqc.MATCHING_INPUT_OUTPUT, True)
    convert_script()

    autopep8_file(filename)

    if args.error_log:
        conversion.output_error_log()


def convert_script():
    """
    Calls separate script depending on script input format
    :return: None
    """

    if not os.path.exists(args.input_filename):
        error_cqc.process_error(error_cqc.INPUT_FILE_NOT_FOUND, True)
    set_output_filename()
    autopep8_file(str(args.input_filename))

    if args.input_format == "projectq":
        process_projectq.process_projectq(args, filename)
    elif args.input_format == "qutip":
        process_qutip.process_qutip(args, filename)
    elif args.input_format == "qiskit":
        process_qiskit.process_qiskit(args, filename)


def set_output_filename():
    """
    Checks for user defined output filename. If none set, use default
    File format set based on user chosen output format
    :return: None
    """

    global filename
    # No user-set filename - use default
    if args.output_filename is None:
        filename = str("convertqc_result")
    else:
        # Checks for invalid filename characters, throwing fatal error if so
        if any(false_char in args.output_filename for false_char in error_cqc.forbidden_filename_chars):
            error_cqc.process_error(error_cqc.OUTPUT_FILENAME_INVALID_CHARACTER, True)
        elif args.debug:
            print("Output filename valid")
        filename = str(args.output_filename)

    # Set the file extension. Currently only one option, but easy to expand in future
    if args.output_format == "qutip" or args.output_format == "projectq" or args.output_format == "qiskit":
        filename += ".py"
        if args.debug:
            print("Output filename: ", filename)


def autopep8_file(name):
    """
    Runs autopep8 on specified filename
    :param name: Filename to run autopep8 on (must be string)
    :return:
    """

    command = "autopep8 " + name + " --in-place --aggressive --aggressive"
    os.system(command)


def process_args():
    """
    Creates the ArgumentParser to handle input arguments.
    Future arguments are easily added with a new .add_argument() line
    :return: None
    """

    global args
    parser = argparse.ArgumentParser(
        description="Convert quantum circuits into different environments")

    # Reguired - input filename
    parser.add_argument("input_filename", help="input filename")
    # Required - input format
    parser.add_argument(
        "input_format",
        help="input format of your script",
        choices=valid_program_types)
    # Required - output format
    parser.add_argument(
        "output_format",
        help="output format of your script",
        choices=valid_program_types)

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

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.debug:
        args.verbose = True


if __name__ == "__main__":
    main()
