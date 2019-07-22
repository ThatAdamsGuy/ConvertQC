from projectq.ops import H, Measure, X, Z
from projectq import MainEngine

# create a main compiler engine
eng = MainEngine()

# allocate one qubit
q1 = eng.allocate_qubit()
q2 = eng.allocate_qubit()

# put it in superposition
H | q1

# measure
Measure | q1

# this is a test of import in the comments
# comment included to test .allocate_qubit() in a comment
# same again but without leading space .allocate_qubit()
# do some random shit
X | q2
Y | q2

R(1.2) | q2


eng.flush()
# print the result:
print("Measured: {}".format(int(q1)))
