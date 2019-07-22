#    Unit tests for conversion.py.
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

import sys
import os
import unittest

sys.path.insert(0, '../convertqc')
from convertqc import conversion

print("RUNNING TESTS - conversion.py")


class ChompTests(unittest.TestCase):
    def test_successful_rn_chomp(self):
        """
        Test - chomp a line with a carriage return and newline character
        :return:
        """
        line = "This is some text"
        new_line = conversion.chomp(line + "\r\n")
        self.assertEqual(line, new_line)

    def test_successful_r_and_n_chomp(self):
        line = "This is some text"
        new_line = conversion.chomp(line + "\r")
        self.assertEqual(line, new_line)

        line = "This is some text"
        new_line = conversion.chomp(line + "\n")
        self.assertEqual(line, new_line)

    def test_successful_no_break_chomp(self):
        line = "This is some text"
        new_line = conversion.chomp(line)
        self.assertEqual(line, new_line)


class FileIOTests(unittest.TestCase):
    def test_successful_file_read(self):
        expected_list = ['these', 'are', 'some', 'lines']
        filename = os.path.join(os.path.dirname(__file__), 'supporting_files/misc/misc_lines.txt')

        list = conversion.read_input_file(filename)
        for i, each in enumerate(list):
            list[i] = conversion.chomp(each)
        self.assertListEqual(list, expected_list)

    @unittest.expectedFailure
    def test_unsuccessful_file_read(self):
        filename = "file_that_does_not_exist.txt"
        conversion.read_input_file(filename)

    def test_successful_open_and_close_output_file(self):
        filename = "test_output.txt"
        file = conversion.open_output_file(filename)
        self.assertIsNotNone(file)
        self.assertFalse(file.closed)
        conversion.close_output_file(file)
        self.assertTrue(file.closed)


class ErrorLogTests(unittest.TestCase):
    def test_successful_add_error_line(self):
        cur_line_no = 7
        text = "Test"
        conversion.add_new_error_line(cur_line_no, text)

        list = conversion.get_error_lines()
        self.assertEqual("7 - Test", list[0])

    @unittest.expectedFailure
    def test_unsuccessful_add_error_line(self):
        cur_line_no = 7
        text = "Test"
        conversion.add_new_error_line(text)
        conversion.add_new_error_line(cur_line_no)


class CopyrightTests(unittest.TestCase):
    def test_writing_copyright(self):
        expected_copyright_notice = [
            '######################################################################',
            '#                                                                    #',
            '# This file has been auto-generated as part of convert_qc.py         #',
            '# There may be errors, mis-translations, or other mistakes           #',
            '# This file is presented as-is, with no guarantee of support, and is #',
            '#     covered under the GNU GPL v3.0 License                         #',
            '# I recommend giving a careful read to check before running          #',
            '#                                                                    #',
            '# For any questions or comments, please email convertqc@gmail.com    #',
            '# For citations, please pretend I wrote an academic paper            #',
            '#                                                                    #',
            '# Input format: QuTiP                                                #',
            '# Output format: ProjectQ                                            #',
            '#                                                                    #',
            '######################################################################'
            ]

        file = open("test.txt", "w+")
        conversion.write_output_copyright(file, "QuTiP", "ProjectQ")
        file.close()

        self.assertTrue(file.closed)

        with open("test.txt") as f:
            input = f.readlines()

        for i, each in enumerate(input):
            input[i] = conversion.chomp(each)

        self.assertListEqual(input, expected_copyright_notice)
