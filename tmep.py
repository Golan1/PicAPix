
DIMACS="""
c An example formula
c
p cnf 3 4
1 2 3 0
-1 2 3 0
1 -2 3 0
1 2 -3 0
"""



clauses, summary, vars_, sat_vars, solver = minisat.create_dimacs_solver(DIMACS)
assert summary == ['p cnf 3 4']
assert len(clauses) == 4
assert len(vars_) == 3
assert solver.solve() is True