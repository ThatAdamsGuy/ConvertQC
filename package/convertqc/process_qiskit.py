from . import conversion, error_cqc

args = None
filename = ""
output_file = None
file_as_list = []


def process_qiskit(input_args, output_filename):
    """
    Entry point for converting from Qiskit
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

    output_file = conversion.open_output_file(filename)
    file_as_list = conversion.read_input_file(args.input_filename)
    conversion.write_output_copyright(output_file, "ProjectQ", "QuTiP")
    print_imports()
    convert_script()
    conversion.close_output_file(output_file)


def print_imports():
    print("In progress!")


def convert_script():
    print("This module was added to test integration of a new conversion language.")
    print("Functionality to convert to/from Qiskit is a work in progress")
