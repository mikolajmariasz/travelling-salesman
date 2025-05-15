import time
import pandas as pd
import numpy as np
from solver.distance_matrix import calculate_distance_matrix
from solver.gurobi_solver import solve_tsp_gurobi
from solver.ortools_solver import solve_tsp_ortools_mip
from solver.simulated_annealing_solver import solve_tsp_simulated_annealing

def performance_analysis(city_list, coordinates, max_cities=25, step=5, time_limit=600):
    """
    Analiza wydajności dla różnych rozmiarów problemu TSP.
    Zwraca DataFrame z wynikami czasu i jakości rozwiązania dla Gurobi i OR-Tools.
    """
    sizes = list(range(5, min(max_cities, len(city_list)) + 1, step))
    results = []

    for size in sizes:
        print(f"\nAnaliza dla {size} miast...")
        selected_cities = city_list[:size]
        dist_matrix = calculate_distance_matrix(selected_cities, coordinates)

        print("  Gurobi...")
        _, gurobi_dist, gurobi_time, gurobi_gap = solve_tsp_gurobi(dist_matrix, time_limit=time_limit)

        print("  OR-Tools...")
        _, ortools_dist, ortools_time = solve_tsp_ortools_mip(dist_matrix, time_limit=time_limit)

        print("  Simulated Annealing...")
        sa_route, sa_dist, sa_time = solve_tsp_simulated_annealing(dist_matrix)

        results.append({
            'size': size,
            'gurobi_distance': gurobi_dist,
            'gurobi_time': gurobi_time,
            'gurobi_gap': gurobi_gap,
            'ortools_distance': ortools_dist,
            'ortools_time': ortools_time,
            'sa_distance': sa_dist,
            'sa_time': sa_time
        })

    return pd.DataFrame(results)
