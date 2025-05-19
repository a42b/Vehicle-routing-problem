import math
import random
import numpy as np
from utils import calculate_distance_matrix

class VRPAnt:
    def __init__(self, customers, demands, capacity):
        self.customers = customers
        self.demands = demands
        self.capacity = capacity
        self.routes = []
        self.total_distance = 0

    def build_solution(self, depot_id, distance_matrix, pheromone, alpha=1, beta=3):
        unvisited = set([c["id"] for c in self.customers])
        routes = []
        while unvisited:
            current_route = [depot_id]
            current_load = 0
            current = depot_id

            while True:
                feasible = [cid for cid in unvisited if current_load + self.demands[cid] <= self.capacity]
                if not feasible:
                    break

                probs = []
                for cid in feasible:
                    tau = pheromone[current][cid] ** alpha
                    eta = (1 / distance_matrix[current][cid]) ** beta
                    probs.append(tau * eta)

                total = sum(probs)
                if total == 0:
                    break
                probs = [p / total for p in probs]
                next_node = random.choices(feasible, weights=probs)[0]

                current_route.append(next_node)
                current_load += self.demands[next_node]
                unvisited.remove(next_node)
                current = next_node

            current_route.append(depot_id)
            routes.append(current_route)

        self.routes = routes
        self.total_distance = self.compute_total_distance(distance_matrix)

    def compute_total_distance(self, distance_matrix):
        dist = 0
        for route in self.routes:
            for i in range(len(route) - 1):
                dist += distance_matrix[route[i]][route[i + 1]]
        return dist


def ant_solver_vrp(data, ants=10, max_iter=100, alpha=1, beta=3, Q=100, rho=0.5):
    depot = data["depot"]
    customers = data["customers"]
    demands = data["demands"]
    capacity = data["capacity"]

    all_nodes = [depot] + customers
    node_ids = [node["id"] for node in all_nodes]
    distance_matrix = calculate_distance_matrix(all_nodes)
    pheromone = {i: {j: 1.0 for j in node_ids} for i in node_ids}

    best_solution = None
    best_cost = float("inf")
    cost_history = []

    for it in range(max_iter):
        solutions = []
        for _ in range(ants):
            ant = VRPAnt(customers, demands, capacity)
            ant.build_solution(depot["id"], distance_matrix, pheromone, alpha, beta)
            solutions.append(ant)

        solutions.sort(key=lambda a: a.total_distance)
        best_ant = solutions[0]

        if best_ant.total_distance < best_cost:
            best_cost = best_ant.total_distance
            best_solution = best_ant.routes

        for i in pheromone:
            for j in pheromone[i]:
                pheromone[i][j] *= (1 - rho)

        for route in best_ant.routes:
            for i in range(len(route) - 1):
                a = route[i]
                b = route[i + 1]
                pheromone[a][b] += Q / best_ant.total_distance
                pheromone[b][a] += Q / best_ant.total_distance

        cost_history.append(best_cost)

        print(f"{it:4}, {best_ant.total_distance:.4f}")

    return best_solution, best_cost, cost_history
