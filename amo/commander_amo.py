from pysat.solvers import Solver
import pairwise_amo

def encode(literals: list, current_id: int = None) -> list:
    group_size = 3
    size = len(literals)
    if size <= 1:
        return [[], [], current_id if current_id is not None else 0]
    groups = []
    current = []
    count = 0
    for i in range(size):
        if count > group_size:
            count = 0
            groups.append(current)
            current = [literals[i]]
        else:
            current.append(literals[i])
            count += 1
    if current is not None:
        groups.append(current)
    if current_id is None:
        current_id = max(literals) if size > 1 else 0
    au_literals = [current_id + i for i in range(1, len(groups)+1)]
    new_id = current_id + len(groups)
    clauses = pairwise_amo.encode(au_literals)[0]
    for g in groups:
        clauses.extend(pairwise_amo.encode(g)[0])
    for i in range(len(groups)):
        for x in groups[i]:
            clauses.append([-x, au_literals[i]])
        clauses.append([-au_literals[i]] + groups[i])
    return [clauses, au_literals, new_id]

def solve(model_name: str, literals: list, group_size: int) -> None:
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
    test = [1,2,3,4,5,6]
    solve('cadical153', test, 3)