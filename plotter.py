import matplotlib.pyplot as plt

def plot_convergence(cost_history, filename="results/convergence.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(cost_history, label="Best Cost So Far")
    plt.xlabel("Iteration")
    plt.ylabel("Total Distance")
    plt.title("ACO Convergence Over Iterations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
