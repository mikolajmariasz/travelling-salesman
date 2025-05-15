from data.coordinates import get_city_coordinates
from utils.performance_analysis import performance_analysis
from utils.plotting import plot_route, plot_analysis, save_analysis_data

from solver.distance_matrix import calculate_distance_matrix
from solver.gurobi_solver import solve_tsp_gurobi
from solver.ortools_solver import solve_tsp_ortools_mip
from solver.simulated_annealing_solver import solve_tsp_simulated_annealing
from config import GUROBI_TIME_LIMIT, ORTOOLS_TIME_LIMIT, SA_TIME_LIMIT, polish_cities

def main():
    coordinates = get_city_coordinates(polish_cities)

    perf_df = performance_analysis(polish_cities, coordinates, max_cities=40, step=5)

    plot_analysis(perf_df)
    save_analysis_data(perf_df)

    dist_matrix = calculate_distance_matrix(polish_cities, coordinates)
    
    # Gurobi Route
    route, dist, _, _ = solve_tsp_gurobi(dist_matrix, time_limit=GUROBI_TIME_LIMIT)
    plot_route(route, polish_cities, coordinates, title=f"Najlepsza trasa Gurobi ({dist:.2f} km)")

    # ORTools Route
    route, dist, _ = solve_tsp_ortools_mip(dist_matrix, time_limit=ORTOOLS_TIME_LIMIT)
    plot_route(route, polish_cities, coordinates, title=f"Najlepsza trasa ORTools ({dist:.2f} km)")

    # Simulated Annealing Route
    route, dist, _ = solve_tsp_simulated_annealing(dist_matrix)
    plot_route(route, polish_cities, coordinates, title=f"Najlepsza trasa Symulowane Wyżarzanie ({dist:.2f} km)")

if __name__ == "__main__":
    main()
