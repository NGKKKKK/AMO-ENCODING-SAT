from ortools.linear_solver import pywraplp

# 1. Khởi tạo solver ILP/MIP (dùng backend SCIP/CBC)
solver = pywraplp.Solver.CreateSolver("CBC")

# 2. Biến quyết định nguyên x, y >= 0
x = solver.IntVar(0, solver.infinity(), "x")
y = solver.IntVar(0, solver.infinity(), "y")

# 3. Ràng buộc tuyến tính
solver.Add(x + 2 * y <= 14)
solver.Add(3 * x - y >= 0)
solver.Add(x - y <= 2)

# 4. Hàm mục tiêu
solver.Maximize(3 * x + 4 * y)

# Giải bài toán
status = solver.Solve()
print(status, '\n', solver.Objective().Value(), '\n' ,f'{x.solution_value()}, {y.solution_value()}')