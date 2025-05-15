import time

def solve_tsp_ortools_mip(distance_matrix, time_limit=120):
    from ortools.linear_solver import pywraplp

    n = distance_matrix.shape[0]
    solver = pywraplp.Solver.CreateSolver('CBC') 
    if not solver:
        print("Nie udało się stworzyć solvera OR-Tools.")
        return None, None, None

    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = solver.BoolVar(f'x[{i},{j}]')

    u = {}
    for i in range(n):
        u[i] = solver.NumVar(0, n - 1, f'u[{i}]')

    solver.Minimize(solver.Sum(distance_matrix[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j))

    for i in range(n):
        solver.Add(solver.Sum(x[i, j] for j in range(n) if i != j) == 1)
        solver.Add(solver.Sum(x[j, i] for j in range(n) if i != j) == 1)

    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)

    start_time = time.time()
    solver.SetTimeLimit(time_limit * 1000) 
    status = solver.Solve()
    end_time = time.time()

    if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        solution = []
        for i in range(n):
            for j in range(n):
                if i != j and x[i, j].solution_value() > 0.5:
                    solution.append((i, j))

        route = [0]
        visited = set(route)
        current = 0
        while len(visited) < n:
            for i, j in solution:
                if i == current and j not in visited:
                    route.append(j)
                    visited.add(j)
                    current = j
                    break

        total_distance = sum(distance_matrix[i][j] for i, j in zip(route, route[1:] + [route[0]]))
        return route, total_distance, end_time - start_time
    else:
        print("Nie znaleziono rozwiązania OR-Tools MIP.")
        return None, None, None