from pysat.solvers import Solver
import pairwise_amo, bitwise_amo


# Solve sudoku board n² x n²
def solve_n_sudoku(board: list, n: int, type_amo=pairwise_amo, name_amo='Pairwise') -> None:
    # Initialization
    size = n*n
    clauses = []
    current_id = size*size*size
    def get_id(x: int, y: int, value: int) -> int:
        return x*size*size + y*size + value
    literals = set(get_id(i, j, value) for i in range(size) for j in range(size) for value in range(1, size+1))
    def add_exactly_one(literals_: list) -> None:
        nonlocal current_id
        clauses.append(literals_) # ALO
        cl, au, current_id = type_amo.encode(literals_, current_id)
        clauses.extend(cl)

    # Cell constraint
    for r in range(size):
        for c in range(size):
            add_exactly_one([get_id(r, c, value) for value in range(1, size+1)])

    # Row constraint
    for c in range(size):
        for value in range(1, size+1):
            add_exactly_one([get_id(r, c, value) for r in range(size)])

    # Column constraint
    for r in range(size):
        for value in range(1, size+1):
            add_exactly_one([get_id(r, c, value) for c in range(size)])

    # Sub-board constraint (n x n)
    for sr in range(n):
        for sc in range(n):
            for value in range(1, size+1):
                lits = []
                for offset_r in range(n):
                    for offset_c in range(n):
                        r = sr*n + offset_r
                        c = sc*n + offset_c
                        lits.append(get_id(r, c, value))
                add_exactly_one(lits)

    # For some pre-numbered cells
    for r in range(size):
        for c in range(size):
            value = board[r][c]
            if value != 0:
                clauses.append([get_id(r, c, value)])

    # Solve
    print(f'Type of AMO: {name_amo}')
    solver = Solver(name='glucose4')
    try:
        for c in clauses:
            solver.add_clause(c)
        if solver.solve():
            model = set(solver.get_model())
            result = [(x if x in model else -x) for x in literals]
            print(f'Solution with main literals: {result}')
            # Board Visualization
            for r in range(size):
                for c in range(size):
                    for value in range(1, size+1):
                        if get_id(r, c, value) in model:
                            print(value, end = ' ' if c < size-1 else '\n')
                            break
        else:
            print('No solution found!')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if solver is not None:
            solver.delete()
    print()


if __name__ == "__main__":
    n = 3
    board = [
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [2, 0, 0, 0, 3, 0, 4, 0, 5],
        [0, 6, 7, 0, 8, 0, 0, 1, 0],
        [1, 0, 4, 3, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 2, 8, 0, 6],
        [0, 7, 0, 0, 4, 0, 3, 2, 0],
        [9, 0, 8, 0, 5, 0, 0, 0, 1],
        [0, 0, 0, 7, 0, 0, 0, 0, 0]
    ]
    solve_n_sudoku(board, n, bitwise_amo, name_amo='Bitwise')
