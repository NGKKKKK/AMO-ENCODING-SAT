from pysat.solvers import Solver
import math

def encode(literals: list, k: int, current_id: int = None) -> list:
    size = len(literals)
    if current_id is None:
        current_id = max(literals) if size > 0 else 0
    if size <= 1 or k >= size:
        return [[], [], current_id]
    if k == 0:
        return [[[-x] for x in literals], [], current_id]
    def get_id(x: int, y: int) -> int:
        return x * k + y + current_id + 1
    new_id = current_id + (size - 1) * k
    au_literals = [[get_id(i, j) for j in range(k)] for i in range(size - 1)]
    clauses = [[-literals[0], au_literals[0][0]]]
    for i in range(1, size - 1):
        x = literals[i]
        clauses.append([-x, au_literals[i][0]])
        for j in range(k):
            clauses.append([-au_literals[i-1][j], au_literals[i][j]])
        for j in range(1, k):
            clauses.append([-au_literals[i-1][j-1], -x, au_literals[i][j]])
    for i in range(1, size):
        x = literals[i]
        clauses.append([-x, -au_literals[i-1][k-1]])
    return [clauses, [e for au in au_literals for e in au], new_id]

def solve(model_name: str, literals: list, k: int) -> None:
    clauses, au_literals, new_id = encode(literals, k)
    print(f'Main literals: {literals} \nAuxiliary literals: {au_literals}\nClauses: {clauses}')
    solver = Solver(name=model_name)
    try:
        for c in clauses:
            solver.add_clause(c)
        solver.add_clause([literals[0]])
        solver.add_clause([literals[1]])
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
    test = [1,2,3,4,5,6,7,8]
    solve('glucose4', test, 1)