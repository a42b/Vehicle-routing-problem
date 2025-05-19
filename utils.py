import math

def euclidean_distance(x1, y1, x2, y2):
    return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2), 2)

def calculate_distance_matrix(nodes):
    distance_matrix = {}
    for i in nodes:
        distance_matrix[i['id']] = {}
        for j in nodes:
            distance_matrix[i['id']][j['id']] = euclidean_distance(i['x'], i['y'], j['x'], j['y'])
    return distance_matrix
