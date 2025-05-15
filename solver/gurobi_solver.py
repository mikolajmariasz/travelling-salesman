import gurobipy as gp
from gurobipy import GRB
import time

def solve_tsp_gurobi(distance_matrix, time_limit=300):
    n = distance_matrix.shape[0]

    try:
        model = gp.Model("TSP")
        model.Params.LogToConsole = 0
        model.Params.TimeLimit = time_limit

        x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
        u = model.addVars(n, vtype=GRB.CONTINUOUS, name="u")

        model.setObjective(gp.quicksum(distance_matrix[i, j] * x[i, j]
                                       for i in range(n) for j in range(n)), GRB.MINIMIZE)

        model.addConstrs((gp.quicksum(x[i, j] for j in range(n) if i != j) == 1 for i in range(n)))
        model.addConstrs((gp.quicksum(x[j, i] for j in range(n) if i != j) == 1 for i in range(n)))
        model.addConstrs((u[i] - u[j] + n * x[i, j] <= n - 1
                          for i in range(1, n) for j in range(1, n) if i != j))

        start = time.time()
        model.optimize()
        end = time.time()

        if model.SolCount > 0:
            route = [0]
            current = 0
            visited = set([0])
            while len(visited) < n:
                for j in range(n):
                    if x[current, j].X > 0.5 and j not in visited:
                        route.append(j)
                        visited.add(j)
                        current = j
                        break
            return route, model.ObjVal, end - start, model.MIPGap

        return None, None, None, None

    except Exception as e:
        print(f"Błąd Gurobi: {e}")
        return None, None, None, None
