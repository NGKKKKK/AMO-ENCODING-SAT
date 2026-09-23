from pysat.solvers import Solver
from amk import sequential_counter_amk

def encode(literals: list, k: int, current_id: int = None) -> list:
    size = len(literals)
    if current_id is None:
        current_id = max(literals) if size > 0 else 0
    if k < 0:
        return [[[]], [], current_id]
    if k == 0:
        return [[], [], current_id]
    if k > size:
        return [[[]], [], current_id]
    if k == size:
        return [[[x] for x in literals], [], current_id]
    if k == 1:
        return [[[x for x in literals]], [], current_id]
    return sequential_counter_amk.encode([-lit for lit in literals], size-k, current_id)

def solve(model_name: str, literals: list, k: int) -> None:
    clauses, au_literals, new_id = encode(literals, k)
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
    test = [1,2,3,4,5,6,7,8]
    solve('glucose4', test, 8)
