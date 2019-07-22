#    Generic conversion functions for ConvertQC
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

import re
error_lines = []


# Source - https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
def read_input_file(filename):
    """
    Reads the specified input filename to a list of lines
    :param filename: Name of file to open
    :return: Line of input file as a list
    """
    with open(filename) as f:
        return f.readlines()


def open_output_file(filename):
    """
    Opens the output file to write converted lines to
    :param filename: Name of file to open
    :return: Output file, as a File object
    """
    return open(filename, "w+")


def close_output_file(file):
    """
    Close the output file at end of conversion
    :param file: File object to close
    :return: Boolean success of closing file
    """
    return file.close()


def add_new_error_line(line_no, untranslated_line):
    """

    :param line_no: Line number in input file which failed to translate
    :param untranslated_line: Untranslated line
    :return: None
    """
    line = str(line_no) + " - " + chomp(str(untranslated_line).strip())
    error_lines.append(line)


def get_error_lines():
    """
    Returns the dictionary of files unable to be translated
    :return: Dictionary of line numbers and untranslated lines
    """
    return error_lines


def output_error_log():
    """
    Opens the error log file, outputs the failed lines, closes file
    :return: None
    """
    error_file = open("error_log.txt", "w+")
    for line in error_lines:
        print(line, file=error_file)
    error_file.close()


# Writes disclaimer at beginning of output file
# Includes contact details, a warning, and a "not my problem" message
def write_output_copyright(output_file, input_format, output_format):
    """
    Write disclaimer at beginning of output file.
    Contains contact details, warranty warning, etc.
    :param output_file: Output file to write to
    :param input_format: Input script format (ProjectQ, QuTiP, etc.)
    :param output_format: Output script format (ProjectQ, QuTiP, etc.)
    :return:
    """
    print(
        "######################################################################",
        file=output_file)
    print(
        "#                                                                    #",
        file=output_file)
    print(
        "# This file has been auto-generated as part of convert_qc.py         #",
        file=output_file)
    print(
        "# There may be errors, mis-translations, or other mistakes           #",
        file=output_file)
    print(
        "# This file is presented as-is, with no guarantee of support, and is #",
        file=output_file)
    print(
        "#     covered under the GNU GPL v3.0 License                         #",
        file=output_file)
    print(
        "# I recommend giving a careful read to check before running          #",
        file=output_file)
    print(
        "#                                                                    #",
        file=output_file)
    print(
        "# For any questions or comments, please email convertqc@gmail.com    #",
        file=output_file)
    print(
        "# For citations, please pretend I wrote an academic paper            #",
        file=output_file)
    print(
        "#                                                                    #",
        file=output_file)

    new_line = "# Input format: " + input_format
    while len(new_line) < 69:
        new_line += " "
    new_line += "#"
    print(new_line, file=output_file)

    new_line = "# Output format: " + output_format
    while len(new_line) < 69:
        new_line += " "
    new_line += "#"
    print(new_line, file=output_file)

    print(
        "#                                                                    #",
        file=output_file)
    print(
        "######################################################################",
        file=output_file)


def untranslateable_line(line, line_no, mark, file):
    if mark:
        print("# *!* ERROR - COULD NOT TRANSFER LINE BELOW COMMENT. PLEASE CHECK MANUALLY: *!* \n" + str(line),
              file=file)
    add_new_error_line(line_no, line)


def debug_print(number, text):
    print(str(number) + " DEBUG: " + text)


def verbose_print(number, text):
    print(str(number) + ": " + text)


# Source -
# https://stackoverflow.com/questions/2268532/grab-a-lines-whitespace-indention-with-python
def get_leading_spaces(line):
    """
    Get the line's leading whitespace via regex
    Useful when outputting translated lines to ensure control kept appropriately
    :param line: Whitespace
    :return: Leading whitespace of input line
    """
    return chomp(re.match(r"\s*", line).group())


# Source -
# https://stackoverflow.com/questions/275018/how-can-i-remove-a-trailing-newline-in-python
def chomp(x):
    """
    Remove trailing line breaks in a system-independent string
    :param x: String to chomp
    :return: String with no trailing linebreaks
    """
    if x.endswith("\r\n"):
        return x[:-2]
    if x.endswith("\n") or x.endswith("\r"):
        return x[:-1]
    return x
