from pysat.solvers import Solver
import pairwise_amo, bitwise_amo, commander_amo, sequential_amo, product_amo

def solve_n_queens(n: int, type_amo=pairwise_amo, name_amo='Pairwise') -> None:
    # Initialization
    board = [[i*n + j + 1 for j in range(n)] for i in range(n)]
    literals = [e for row in board for e in row]
    current_id = n * n
    clauses = []

    # Row constraint
    for r in range(n):
        row_literals = board[r]
        clauses.append(row_literals) # ALO
        c, au, current_id = type_amo.encode(row_literals, current_id)
        clauses.extend(c)

    # Column constraint
    for c in range(n):
        column_literals = [board[r][c] for r in range(n)]
        c_cls, au, current_id = type_amo.encode(column_literals, current_id)
        clauses.extend(c_cls)

    # Diag constraint
    diag_size = 2*n - 1
    main_diags = [[] for i in range(diag_size)]
    sub_diags = [[] for i in range(diag_size)]
    for r in range(n):
        for c in range(n):
            m = r-c+(n-1)
            main_diags[m].append(board[r][c])
            s = r+c
            sub_diags[s].append(board[r][c])
    for e in main_diags:
        if len(e) > 1:
            c, au, current_id = type_amo.encode(e, current_id)
            clauses.extend(c)
    for e in sub_diags:
        if len(e) > 1:
            c, au, current_id = type_amo.encode(e, current_id)
            clauses.extend(c)

    # Solve
    print(f'Type of AMO: {name_amo}')
    solver = Solver(name='glucose4')
    try:
        for c in clauses:
            solver.add_clause(c)
        if solver.solve():
            model = solver.get_model()
            # print(f'Solution with auxiliary literals: {model}')
            result = [(x if x in model else -x) for x in literals]
            print(f'Solution with main literals: {result}')
        else:
            print('No solution found!')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if solver is not None:
            solver.delete()
    print()

if __name__ == '__main__':
    solve_n_queens(4)
    solve_n_queens(4, bitwise_amo, name_amo='Bitwise')
    solve_n_queens(4, commander_amo, name_amo='Commander')
    solve_n_queens(4, sequential_amo, name_amo='Sequential')
    solve_n_queens(4, product_amo, name_amo='Commander')