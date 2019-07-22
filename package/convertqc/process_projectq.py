#    Functions for translating from ProjectQ to QuTiP
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
import re
from . import conversion
import ast

file_as_list = []
args = None
filename = ""
output_file = None
qubits = []
current_function = ""
line_is_expression = False
dagger_next_line = False
meta_whitespace = ""
current_line_no = 0


def process_projectq(input_args, output_filename):
    """
    Entry point for converting from ProjectQ
    :param input_args: Input arguments from command line call
    :param output_filename: Desired name of output file
    :return: None
    """
    global args
    global filename
    global output_file
    global file_as_list
    args = input_args
    filename = output_filename
    if args.verbose:
        print("Processing ProjectQ input file...")

    output_file = conversion.open_output_file(filename)
    file_as_list = conversion.read_input_file(args.input_filename)
    conversion.write_output_copyright(output_file, "ProjectQ", "QuTiP")
    print_imports()
    convert_script()
    conversion.close_output_file(output_file)


def check_for_qubits():
    """
    Searches the input file for relevant lines adding qubits to a system
    :return: Number of qubits
    """
    qubit_count = 0
    for line in file_as_list:
        if ".allocate_qubit()" in line and line[0] is not "#":
            qubit_count += 1
            qubits.append(line.strip().split()[0])
    if args.verbose:
        conversion.verbose_print(current_line_no, "Qubits counted: " + str(qubit_count))
    return qubit_count


def convert_gate(line):
    """
    Convert quantum gates into appropriate format
    :param line: Line to translate
    :return: None
    """
    whitespace = conversion.get_leading_spaces(line)

    split_line = line.strip().split()
    gate = split_line[0]
    if args.debug:
        print("Gate - " + gate)

    # Pauli-X
    if gate == "X":
        qubit = get_qubit_from_list(split_line[2])
        rotation_gate(whitespace, "X", qubit, "pi")
    # Pauli-Y
    elif gate == "Y":
        qubit = get_qubit_from_list(split_line[2])
        rotation_gate(whitespace, "Y", qubit, "pi")
    # Pauli-Z
    elif gate == "Z":
        qubit = get_qubit_from_list(split_line[2])
        rotation_gate(whitespace, "Z", qubit, "pi")
    elif gate == "H":
        print(whitespace +
              "quantum_circuit.add_gate(\"SNOT\", " +
              str(get_qubit_from_list(split_line[2])) +
              ")", file=output_file, end='')
    # elif gate == "Measure":
    # print("TEMPORARY MEASURE")
    elif gate == "CNOT":
        invalid_chars = "(,) "
        qubit_one = split_line[2]
        qubit_two = split_line[3]
        for char in invalid_chars:
            qubit_one = qubit_one.replace(char, "")
        for char in invalid_chars:
            qubit_two = qubit_two.replace(char, "")
        print(
            whitespace +
            "quantum_circuit.add_gate(\"CNOT\", " +
            qubit_one +
            ", " +
            qubit_two +
            ")",
            file=output_file,
            end='')
    # Non-Pauli Rotation Gate
    elif gate[0] == "R" and (gate[1] == "x" or gate[1] == "y" or gate[1] == "z"):
        # Find the string between the two brackets
        angle = gate[gate.find("(") + 1:gate.find(")")]
        rotation_gate(
            whitespace, str(
                gate[1]).upper(), angle, str(
                get_qubit_from_list(
                    split_line[2])))
    # C-Phase Gate
    elif gate[0] == "R" and (gate[1] == "("):
        if args.mark:
            print("# Unknown formatting of below line: Please manually check", file=output_file)
        rotation = line[line.find("R(")+2:line.find(")")]
        qubit = line[line.find("|")+1:].strip()
        print(conversion.get_leading_spaces(line) + "quantum_circuit.add_gate(\"CPHASE\", " + qubit + ", " + rotation
              + ")", file=output_file)


def rotation_gate(whitespace, orientation, qubit, angle):
    """
    Handles conversion for all rotation gates
    :param whitespace: Whitespace of translated line to maintain control
    :param orientation: Direction of rotation
    :param qubit: Qubit to apply rotation to
    :param angle: Angle of rotation
    :return: None
    """
    if orientation == "X":
        print(
            whitespace +
            "quantum_circuit.add_gate(\"RX\", " +
            str(qubit) +
            ", " +
            str(angle) +
            ")",
            file=output_file,
            end='')
        if args.debug:
            print(
                "Converted to: quantum_circuit.add_gate(\"RX\", " +
                str(qubit) +
                ", " +
                str(angle) +
                ")", )
    elif orientation == "Y":
        print(
            whitespace +
            "quantum_circuit.add_gate(\"RY\", " +
            str(qubit) +
            ", " +
            str(angle) +
            ")",
            file=output_file,
            end='')
        if args.debug:
            print(
                "Converted to: quantum_circuit.add_gate(\"RY\", " +
                str(qubit) +
                ", " +
                str(angle) +
                ")", )
    elif orientation == "Z":
        print(
            whitespace +
            "quantum_circuit.add_gate(\"RZ\", " +
            str(qubit) +
            ", " +
            str(angle) +
            ")",
            file=output_file,
            end='')
        if args.debug:
            print("Converted to: quantum_circuit.add_gate(\"RZ\", " +
                  str(qubit) +
                  ", " +
                  str(angle) +
                  ")")


def get_qubit_from_list(qubit_name):
    """
    ProjectQ qubits are named objects, whilst QuTiP is a position in an array
    This function converts from object to position based on the list from earlier
    :param qubit_name: Name of qubit in ProjectQ
    :return: Position of input qubit in array
    """
    try:
        # Qubit in the list found by searching input file
        return qubits.index(qubit_name)
    except BaseException:
        # Qubit not in list - possible function parameter

        # https://stackoverflow.com/questions/1059559/split-strings-into-words-with-multiple-word-boundary-delimiters
        split_line = re.findall(r"[\w']+", qubit_name)
        if qubit_name in split_line:
            return qubit_name


def process_variable_definition(line):
    """
    Checks for certain lines and whether they're needed in QuTiP.
    Will later be expanded
    :param line: Line to convert
    :return: True if conversion needed, False otherwise
    """
    if "allocate_qubit(" in line:
        # Allocate qubit not needed in QuTiP
        return False
    else:
        return True


def convert_script():
    """
    Run through all input lines and convert (if able) to desired output
    :return: None
    """
    global current_function
    # Flag to add a dagger (inversion) to next line
    global dagger_next_line

    global current_line_no

    defined_variables = []

    current_line_no = 1

    for line in file_as_list:
        sys.stdout.flush()
        split_line = line.split()
        whitespace = conversion.get_leading_spaces(line)
        new_line = whitespace + line.strip()

        # empty line
        if not split_line:
            print(file=output_file, end='')
        else:
            if args.verbose:
                print()
                print(current_line_no, end='')
                print(": " + line.rstrip())

            # function definition
            if split_line[0] == "def":
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Function definition - copying verbatim")
                current_function = line
                defined_variables.clear()
                print(new_line, file=output_file, end='')

            # imports
            elif split_line[0] == "from" or split_line[0] == "import":
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Import statement - ignoring")
                print(file=output_file, end='')

            # comments - copy as standard
            elif split_line[0] == "#":
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Comment - ignoring")
                print(new_line, file=output_file, end='')

            # variable definitions - **
            elif " = " in line:
                defined_variables.append(split_line[0])
                process_variable_definition(line)

            # if statement
            elif split_line[0] == "if":
                if args.verbose:
                    conversion.verbose_print(current_line_no, "If statement - copied verbatim")
                print(new_line, file=output_file, end='')

            # print statements
            elif "print(" in line:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Print statement - copied verbatim")
                print(new_line, file=output_file, end='')

            # pipe operator:
            elif " | " in line:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Gate detected - processing")
                convert_gate(new_line)

            # meta function
            elif "with" in line:
                if args.verbose:
                    print(str(current_line_no) + ": Meta gate (", end='')
                if "Dagger" in line:
                    if args.verbose:
                        print("DAGGER) detected")
                    process_meta_tag(line, "Dagger")
                elif "Control" in line:
                    if args.verbose:
                        print("CONTROL) detected")
                    process_meta_tag(line, "Control")

            # return line
            elif "return " in line:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Return statement - processing")
                process_return(defined_variables, line)

            # function call
            elif check_for_function_call(line.strip()):
                print(new_line, file=output_file, end='')

            else:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Unsure how to translate line. Copying verbatim and "
                                                              "adding to error log")
                conversion.untranslateable_line(current_line_no, line, args.mark, output_file)

            if dagger_next_line is True:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Adding dagger control")
                dagger_next_line = False
                print(".dag()", file=output_file)
            else:
                print(file=output_file)

        current_line_no += 1


def check_for_function_call(line):
    """
    Use abstract syntax tree to identify if line is a function call
    :param line: Line to check
    :return: True if expression, False if not
    """
    global line_is_expression

    if args.verbose:
        conversion.verbose_print(current_line_no, "Checking if line is function call")

    tree = ast.parse(line)
    visitor = Visitor()
    visitor.visit(tree)
    if line_is_expression:
        # Will have been set True by NodeVisitor
        if args.verbose:
            conversion.verbose_print(current_line_no, "Line is function call - copying verbatim")
        line_is_expression = False
        return True
    else:
        return False


def process_return(variables, line):
    """
    Handles return statements
    :param variables: Parameters of function line is part of
    :param line: Line to check
    :return: None
    """
    if not variables:
        if "True" in line or "False" in line:
            print(line, file=output_file)
        else:
            print(conversion.get_leading_spaces(line) + "# Originally returned variables, no longer needed",
                  file=output_file)
    elif any(var in line for var in variables):
        # returning variables defined in function
        print(line, file=output_file)
    else:
        print(conversion.get_leading_spaces(line) + "# Originally returned variables, no longer needed",
              file=output_file)


def process_meta_tag(line, tag):
    """
    Checks meta tags such as Control or Dagger
    :param line: Line to translate
    :param tag: Name of control function to handle
    :return:
    """
    global dagger_next_line
    global meta_whitespace
    global current_meta

    meta_whitespace = conversion.get_leading_spaces(line)
    if tag == "Dagger":
        if args.verbose:
            conversion.verbose_print(current_line_no, "Dagger meta detected")
        current_meta = "Dagger"
        dagger_next_line = True
    if tag == "Control":
        if args.verbose:
            conversion.verbose_print(current_line_no, "Control meta detected")
        current_meta = "Control"


def print_imports():
    """
    Prints required imports for QuTiP
    Future work will extract this to separate conversion file
    :return: None
    """

    if args.verbose:
        conversion.verbose_print(current_line_no, "Printing import statements and basic lines")

    print(file=output_file)
    print("from numpy import pi", file=output_file)
    print("from qutip import *", file=output_file)
    print(file=output_file)
    print("quantum_circuit = QubitCircuit(" +
          str(check_for_qubits()) + ")", file=output_file)
    print(file=output_file)


class Visitor(ast.NodeVisitor):
    """
    Overwrites the NodeVisitor class to perform particular functions based on their type
    """
    def visit_Expr(self, node):
        global line_is_expression
        line_is_expression = True
        self.generic_visit(node)
