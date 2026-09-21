from pysat.solvers import Solver
import math

def encode(literals: list, current_id: int = None) -> list:
    size = len(literals)
    if size <= 1:
        return [[], [], current_id if current_id is not None else 0]
    if current_id is None:
        current_id = max(literals) if size > 1 else 0
    m = math.ceil(math.log2(size))
    au_literals = [current_id + i for i in range(1, m+1)]
    new_id = current_id + m
    clauses = []
    for i in range(size):
        x = literals[i]
        for j in range(m):
            au = au_literals[j]
            val = (i >> j) & 1
            if val == 1:
                clauses.append([-x, au])
            else:
                clauses.append([-x, -au])
    return [clauses, au_literals, new_id]

def solve(model_name: str, literals: list) -> None:
    clauses, au_literals, new_id = encode(literals)
    print(f'Main literals: {literals} \nAuxiliary literals: {au_literals}\nClauses: {clauses}')
    solver = Solver(name=model_name)
    try:
        for c in clauses:
            solver.add_clause(c)
        if solver.solve():
            model = solver.get_model()
            print(f'Solution with auxiliary literals: {model}')
            result = [(x if x in model else -x) for x in literals]
            print(f'Solution with main literals: {result}')
        else:
            print('No solution found!')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if solver is not None:
            solver.delete()


if __name__ == '__main__':
    test = [1,2,3,4,5]
    solve('glucose4', test)