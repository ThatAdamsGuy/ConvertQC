#    Functions for translating from QuTiP to ProjectQ
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

import ast
import re

from . import conversion
from . import error_cqc

file_as_list = []
qubit_list = []
args = None
output_file = None
current_function = ""
qubit_count = 0
circuit_name = ""
current_line_no = 0


def process_qutip(input_args, output_filename):
    """

    :param input_args: Arguments from program call on command line
    :param output_filename: Name of converted output file
    :return: None
    """
    global args
    global filename
    global output_file
    global file_as_list

    args = input_args
    filename = output_filename

    if args.debug:
        print("Processing QuTiP input file...")

    output_file = conversion.open_output_file(filename)
    file_as_list = conversion.read_input_file(args.input_filename)
    conversion.write_output_copyright(output_file, "QuTiP", "ProjectQ")
    print_imports()
    convert_script()
    print_final_script()
    conversion.close_output_file(output_file)


def convert_script():
    """
    Handles each line of conversion for QuTiP input
    :return: None
    """
    if not check_for_circuit():
        error_cqc.process_error(error_cqc.QUTIP_NO_QUBIT_DEFINITIONS, True)
    global current_function
    global current_line_no

    add_gate = circuit_name + ".add_gate("

    current_line_no = 1

    for line in file_as_list:

        split_line = line.split()
        whitespace = conversion.get_leading_spaces(line)
        new_line = whitespace + line.strip()

        # empty line
        if not split_line:
            print(file=output_file)
        else:
            if args.verbose:
                print()
                print(current_line_no, end='')
                print(": " + line.rstrip())

            # function definition
            if split_line[0] == "def":
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Function defenition - copying verbatim")
                current_function = line
                print(new_line, file=output_file)

            # imports
            elif split_line[0] == "from" or split_line[0] == "import":
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Import statement - ignoring")
                print(file=output_file)

            # comments - copy as standard
            elif split_line[0] == "#":
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Comment - copying verbatim")
                print(new_line, file=output_file)

            # new gate added to circuit
            elif add_gate in line:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Gate detected")
                if not process_gate(line):
                    conversion.untranslateable_line(line, current_line_no, args.mark, output_file)

            # Circuit definition - no equivalent in projectq
            elif " = QubitCircuit(" in line:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "QubitCircuit declaration - ignoring")
                print(file=output_file)

            else:
                if args.verbose:
                    conversion.verbose_print(current_line_no, "Unsure how to translate line. Copying verbatim and "
                                                              "adding to error log")
                conversion.untranslateable_line(line, current_line_no, args.mark, output_file)

        current_line_no += 1


def process_gate(line):
    """
    Translates gates into ProjectQ format
    TODO
    :param line: Line to translate
    :return: None
    """

    # Extract gate from parameters
    gate = line[line.find("(\"")+2:line.find("\",")]
    if args.debug:
        conversion.debug_print(current_line_no, "Gate found: " + gate)

    # CNOT Gate
    if gate == "CNOT":
        return convert_cnot_gate(line)
    # Rotation Gate
    elif gate[0] == "R" and (gate[1] == "X" or "Y" or "Z"):
        return convert_rotation_gate(line, gate[1])
    # Hadamard Gate
    elif gate == "SNOT":
        if args.verbose:
            conversion.verbose_print(current_line_no, "Converting to Hadamard gate")
        qubit = line[line.find(",")+1:line.find(")")].strip()
        print(conversion.get_leading_spaces(line) +  "H | " + get_named_qubit_from_position(qubit), file=output_file)
        return True
    # SWAP Gate
    elif gate == "SWAP":
        return convert_swap_gate(line)
    elif gate == "SQRTSWAP":
        return convert_swap_gate(line, sqrt=True)
    # ISWAP Gate
    elif gate == "ISWAP":
        if args.verbose:
            conversion.verbose_print(current_line_no, "Could not translate ISWAP Gate - No Known ProjectQ Version")
        if args.mark:
            print("# Could not translate ISWAP Gate - No Known ProjectQ Version", file=output_file)
            return True
        else:
            return False
    elif gate == "CPHASE":
        return convert_cphase_gate(line)
    else:
        if args.verbose:
            conversion.verbose_print(current_line_no, "Unsure how to translate line. Copying verbatim")
        return False


def convert_rotation_gate(line, direction):
    if args.verbose:
        conversion.verbose_print(current_line_no, "Converting to Rotation (" + direction.upper() + ") Gate")

    one_param = line[line.find("(") + 1:line.find(")")]
    # parameters between commas
    remaining_params = re.findall(","+"(.*?)"+",", line)
    named_qubit = ""
    rotation = ""

    if "," not in one_param:
        if args.debug:
            print("Only one parameter!")
    elif not remaining_params:
        if args.debug:
            print("Two parameters!")
        # find string between comma and closing parentheses
        named_qubit = get_named_qubit_from_position(line[line.find(",")+1:line.find(")")].strip())
        rotation = "pi"
    else:
        if args.debug:
            print("3+ Params")
        if len(remaining_params) == 2:
            named_qubit = get_named_qubit_from_position(remaining_params[0].strip().replace(" ", ""))
            rotation = remaining_params[1].strip().replace(" ", "")
        else:
            return False

    if rotation == "pi":
        print(conversion.get_leading_spaces(line) + direction.upper() + " | " + named_qubit, file=output_file)
    else:
        print(conversion.get_leading_spaces(line) + "R" + direction.lower() + "(" + rotation + ") | " + named_qubit,
              file=output_file)

    return True


def convert_cnot_gate(line):
    if args.verbose:
        conversion.verbose_print(current_line_no, "Converting to CNOT Gate")
    first_qubit = re.search(',(.*),', line)
    second_qubit = re.search(',(.*)\\)', line)
    new_regex = second_qubit.group(0)[2:]
    new_second_qubit = re.search(',(.*)\\)', new_regex)

    if args.debug:
        conversion.debug_print(current_line_no, "Regex Check")
        conversion.debug_print(current_line_no, line)
        conversion.debug_print(current_line_no, first_qubit.group(0))
        conversion.debug_print(current_line_no, first_qubit.group(1))
        conversion.debug_print(current_line_no, new_second_qubit.group(0).strip())
        conversion.debug_print(current_line_no, new_second_qubit.group(1).strip())

    print(conversion.get_leading_spaces(line) + "CNOT | (" + get_named_qubit_from_position(first_qubit.group(1).strip())
          + ", " + get_named_qubit_from_position(new_second_qubit.group(1).strip()) + ")", file=output_file)
    return True


def convert_swap_gate(line, sqrt=False):
    if args.verbose:
        print(str(current_line_no) + ": Converting to ", end='')
        if sqrt:
            print("SQRT", end='')
        print("SWAP Gate")
    square_brackets = line[line.find("["):line.find("]")+1]
    square_brackets.replace("[", "").replace("]", "")
    qubits = square_brackets.split(",")

    if args.debug:
        conversion.debug_print(current_line_no, "Qubits: " + str(qubits))

    print(conversion.get_leading_spaces(line), end='', file=output_file)
    if sqrt:
        print("SQRT", end='', file=output_file)

    print("SWAP | (", end='', file=output_file)
    for i, each in enumerate(qubits):
        if i != len(qubits) - 1:
            if "[" in each:
                each = each.replace("[", "")
            print(each + ", ", file=output_file, end='')
        else:
            if "]" in each:
                each = each.replace("]", "")
            print(each + ")", file=output_file)

    return True


def convert_cphase_gate(line):
    if args.verbose:
        conversion.verbose_print(current_line_no, "Converting to CPHASE (R()) Gate")
    params = line[line.find("(")+1:line.find(")")].strip().replace(" ", "")
    split_params = params.split(",")
    qubit = split_params[1]

    if args.debug:
        conversion.debug_print(current_line_no, "Qubit: " + qubit)
        conversion.debug_print(current_line_no, "Params: " + str(split_params))

    if split_params[2] != "None":
        rotation = split_params[2]
    else:
        rotation = split_params[3]

    if args.mark:
        print("# Unknown formatting of below line: Please manually check", file=output_file)
    print(conversion.get_leading_spaces(line) + "R(" + rotation + ") | " + get_named_qubit_from_position(qubit),
          file=output_file)

    return True


def get_named_qubit_from_position(qubit):
    if args.debug:
        conversion.debug_print(current_line_no, "Qubit input: " + str(qubit))
        conversion.debug_print(current_line_no, "Returning: qubit_" + str(qubit))
    return "qubit_" + qubit


def check_for_circuit():
    global qubit_list
    global circuit_name

    if args.verbose:
        conversion.verbose_print(current_line_no, "Checking for circuit definition")

    for line in file_as_list:
        if " = QubitCircuit(" in line:
            new_line = line.split()
            circuit_name = new_line[0]
            if args.verbose:
                conversion.verbose_print(current_line_no, "Found circuit definition. Name: " + str(new_line[0]))

            visit = Visitor()
            tree = ast.parse(line)
            visit.visit(tree)
            return True
    return False


def print_imports():
    print(file=output_file)
    print("from projectq import *", file=output_file)
    print(file=output_file)


def print_final_script():
    print(file=output_file)
    print("eng.flush()", file=output_file)
    print(file=output_file)
    print("# TODO - Add desired measurements", file=output_file)
    print(file=output_file)


def set_qubit_count(count):
    global qubit_count
    if args.verbose:
        conversion.verbose_print(current_line_no, "Qubits counted: " + str(ast.literal_eval(count)))
    qubit_count = ast.literal_eval(count)

class Visitor(ast.NodeVisitor):
    def visit_Call(self, node):
        first_arg = node.args[0]
        if isinstance(first_arg, ast.Num):
            set_qubit_count(first_arg)
