import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

def save_analysis_data(df, filename_prefix="tsp_analysis"):
    os.makedirs("results", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/{filename_prefix}_{timestamp}.csv"
    
    df.to_csv(filename, index=False)
    print(f"Dane zapisane do pliku: {filename}")

def plot_analysis(df):
    os.makedirs("results/plots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Wykres 1 - Czasy działania
    plt.figure(figsize=(12, 6))
    plt.plot(df['size'], df['gurobi_time'], label='Gurobi', marker='o', color='tab:blue')
    plt.plot(df['size'], df['sa_time'], label='Simulated Annealing', marker='^', color='tab:green')  
    plt.plot(df['size'], df['ortools_time'], label='OR-Tools', marker='s', color='tab:orange')
    
    plt.xlabel('Liczba miast', fontsize=12)
    plt.ylabel('Czas (s)', fontsize=12)
    plt.title('Czas działania solverów', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    for i, row in df.iterrows():
        plt.text(row['size'], row['gurobi_time'], f"{row['gurobi_time']:.1f}", 
                 ha='center', va='bottom', fontsize=8)
        plt.text(row['size'], row['sa_time'], f"{row['sa_time']:.1f}", 
                 ha='center', va='bottom', fontsize=8)
        plt.text(row['size'], row['ortools_time'], f"{row['ortools_time']:.1f}", 
                 ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    time_plot_filename = f"results/plots/tsp_time_comparison_{timestamp}.png"
    plt.savefig(time_plot_filename, dpi=300, bbox_inches='tight')
    print(f"Wykres czasów zapisany do pliku: {time_plot_filename}")
    plt.show()
    
    # Wykres 2 - Długości tras
    plt.figure(figsize=(12, 6))
    plt.plot(df['size'], df['gurobi_distance'], label='Gurobi', marker='o', color='tab:blue')
    plt.plot(df['size'], df['ortools_distance'], label='OR-Tools', marker='s', color='tab:orange', linestyle='--')
    plt.plot(df['size'], df['sa_distance'], label='Simulated Annealing', marker='^', color='tab:green')
    
    plt.xlabel('Liczba miast', fontsize=12)
    plt.ylabel('Długość trasy (km)', fontsize=12)
    plt.title('Długość znalezionych tras', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    distance_plot_filename = f"results/plots/tsp_distance_comparison_{timestamp}.png"
    plt.savefig(distance_plot_filename, dpi=300, bbox_inches='tight')
    print(f"Wykres długości tras zapisany do pliku: {distance_plot_filename}")
    plt.show()
    
    # Wykres 3 - Różnice czasów
    plt.figure(figsize=(12, 6))
    gurobi_times = df['gurobi_time']
    ortools_times = df['ortools_time']
    sa_times = df['sa_time']
    
    ortools_diff = ortools_times - gurobi_times
    sa_diff = sa_times - gurobi_times
    
    bar_width = 0.35
    index = df['size']
    
    plt.bar(index - bar_width/2, ortools_diff, width=bar_width, 
            label='OR-Tools - Gurobi', color='tab:orange')
    plt.bar(index + bar_width/2, sa_diff, width=bar_width, 
            label='SA - Gurobi', color='tab:green')
    
    plt.xlabel('Liczba miast', fontsize=12)
    plt.ylabel('Różnica czasu (s)', fontsize=12)
    plt.title('Różnica czasu względem Gurobi', fontsize=14)
    plt.axhline(0, color='black', linestyle='--')
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    for i, (ort_diff, sa_diff) in enumerate(zip(ortools_diff, sa_diff)):
        if ort_diff != 0:
            plt.text(index[i] - bar_width/2, ort_diff, f"{ort_diff:.1f}", 
                     ha='center', va='bottom' if ort_diff > 0 else 'top', fontsize=8)
        if sa_diff != 0:
            plt.text(index[i] + bar_width/2, sa_diff, f"{sa_diff:.1f}", 
                     ha='center', va='bottom' if sa_diff > 0 else 'top', fontsize=8)

    plt.tight_layout()
    diff_plot_filename = f"results/plots/tsp_time_diff_{timestamp}.png"
    plt.savefig(diff_plot_filename, dpi=300, bbox_inches='tight')
    print(f"Wykres różnic czasów zapisany do pliku: {diff_plot_filename}")
    plt.show()

def plot_route(route, cities, coordinates, title="Trasa TSP"):
    if not route:
        print("Brak trasy do wyświetlenia.")
        return

    ordered_coords = [coordinates[cities[i]] for i in route]
    x = [coord[1] for coord in ordered_coords]
    y = [coord[0] for coord in ordered_coords]

    plt.figure(figsize=(10, 8))
    plt.plot(x + [x[0]], y + [y[0]], marker='o', linestyle='-', color='tab:blue')
    
    for i, city_index in enumerate(route):
        city_name = cities[city_index]
        plt.text(x[i], y[i], city_name, fontsize=9, ha='center', va='bottom')

    plt.title(title, fontsize=14)
    plt.xlabel("Długość geograficzna", fontsize=12)
    plt.ylabel("Szerokość geograficzna", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    os.makedirs("results/routes", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    route_filename = f"results/routes/tsp_route_{timestamp}.png"
    plt.savefig(route_filename, dpi=300, bbox_inches='tight')
    print(f"Wykres trasy zapisany do pliku: {route_filename}")
    
    plt.show()