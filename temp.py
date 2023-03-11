from z3 import *

Tie, Shirt = Bools('Tie Shirt')
s = Solver()

s.from_file('temp/clauses.dimacs')
print(s.check())
model = s.model()

