import numpy as np
from geopy.distance import geodesic

def calculate_distance_matrix(cities, coordinates):
    n = len(cities)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = geodesic(coordinates[cities[i]], coordinates[cities[j]]).km

    return matrix
