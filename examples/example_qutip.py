from qutip import *
from numpy import pi

circuit = QubitCircuit(3)
circuit.add_gate("CNOT", 0, 1)
circuit.add_gate("SNOT", 2)
circuit.add_gate("CNOT", 2, 1)


def do_some_rotations():
    circuit.add_gate("RX", 1)
    circuit.add_gate("RY", 2)
    circuit.add_gate("RZ", 0)


circuit.add_gate("RZ", 0, None, pi / 2, r"\pi/2")

do_some_rotations()

# SWAP
circuit.add_gate("SWAP", [0, 1], None)
circuit.add_gate("SWAP", [0, 1, 2], None)
circuit.add_gate("SWAP", [0, 1, 2, 3, 4], None)

# SQRTSWAP
circuit.add_gate("SQRTSWAP", [0, 1], None)
circuit.add_gate("SQRTSWAP", [0, 1, 2], None)
circuit.add_gate("SQRTSWAP", [0, 1, 2, 3, 4], None)

# iSWAP
circuit.add_gate("ISWAP", [1, 2])

# CPHASE
circuit.add_gate("CPHASE", 1, None, 1.2 * pi)
