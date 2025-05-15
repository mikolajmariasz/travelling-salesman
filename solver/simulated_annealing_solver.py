import numpy as np
import random
import time

def calculate_route_distance(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1)) + dist_matrix[route[-1]][route[0]]

def solve_tsp_simulated_annealing(dist_matrix, initial_temp=10000, cooling_rate=0.999, 
                                 stop_temp=1e-5, max_iter=50000, n_restarts=3):
    best_route = None
    best_distance = float('inf')
    total_time = 0
    
    for _ in range(n_restarts):
        start_time = time.time()
        n = len(dist_matrix)
        current_route = list(range(n))
        random.shuffle(current_route)  
        current_distance = calculate_route_distance(current_route, dist_matrix)

        temp = initial_temp
        iteration = 0
        
        while temp > stop_temp and iteration < max_iter:
            if random.random() < 0.7: 
                i, j = sorted(random.sample(range(n), 2))
                new_route = current_route[:i] + current_route[i:j+1][::-1] + current_route[j+1:]
            else:  
                i, j = random.sample(range(n), 2)
                new_route = current_route[:]
                new_route[i], new_route[j] = new_route[j], new_route[i]
                
            new_distance = calculate_route_distance(new_route, dist_matrix)
            delta = new_distance - current_distance

            if delta < 0 or random.random() < np.exp(-delta / temp):
                current_route = new_route
                current_distance = new_distance

                if current_distance < best_distance:
                    best_route = current_route[:]
                    best_distance = current_distance

            temp *= cooling_rate
            iteration += 1
        
        total_time += time.time() - start_time

    return best_route, best_distance, total_time
