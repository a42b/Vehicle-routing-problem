from parser import load_xml
from vrp_aco import ant_solver_vrp
from plotter import plot_convergence
import os

INSTANCES = [
    ("data/data_32.xml", "instance1"),
    ("data/data_72.xml", "instance2"),
    ("data/data_422.xml", "instance3")
]

def main():
    for file_path, name in INSTANCES:
        print(f"\nProcessing {name}...")
        data = load_xml(file_path)
        solution, cost, history = ant_solver_vrp(data)

        print(f"Best Cost: {cost}")
        for i, route in enumerate(solution):
            print(f"Vehicle {i+1}: {' -> '.join(map(str, route))}")

        plot_file = f"results/convergence_{name}.png"
        plot_convergence(history, filename=plot_file)
        print(f"Saved convergence graph to {plot_file}")

        route_file = f"results/best_routes_{name}.txt"
        with open(route_file, "w") as f:
            f.write(f"Best Total Cost: {cost:.2f}\n\n")
            for i, route in enumerate(solution):
                f.write(f"Vehicle {i+1}: {' -> '.join(map(str, route))}\n")
        print(f"Saved route details to {route_file}")

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    main()
