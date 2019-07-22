#    Functions for handling error output for ConvertQC
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

# ERROR_CODES
INPUT_FILE_NOT_FOUND = 1
OUTPUT_FILENAME_INVALID_CHARACTER = 2
MATCHING_INPUT_OUTPUT = 3

QUTIP_NO_QUBIT_DEFINITIONS = 21

forbidden_filename_chars = ['/', '<', '>', ':', '"', '\\', '|', '.', '?', '*']


def process_error(code, is_fatal):
    switch = {
        1: "Input file not found",
        2: "Output filename contains invalid characters",
        3: "Input file format matches output file format",
        21: "No qubits allocated in input script"
    }
    print_error(code, switch.get(code), is_fatal)


def print_error(code, error_msg, is_fatal):
    if is_fatal:
        print("FATAL ", end='')
    print("ERROR:")
    print("    Code: " + str(code))
    print("    Message: " + str(error_msg))
    if is_fatal:
        print("\nExiting...")
        exit(code)
