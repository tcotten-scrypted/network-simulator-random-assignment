# AI Attribution: This content was generated in whole or part with the assistance of an AI model.
# Author: Tim Cotten <tim@cotten.io> @cottenio
# 2024-07-05

import argparse
import math
import numpy as np
from collections import defaultdict

np.random.seed(42)

def estimate_network_capacity(N, k, m):
    """
    Estimate the total capacity of the network in terms of the number of tasks
    that can be handled within one frame.

    Args:
        N (int): Total number of nodes in the network.
        k (int): Number of nodes required to handle each task.
        m (int): Maximum number of tasks a single node can handle simultaneously.

    Returns:
        int: The estimated total capacity of the network in terms of the number of tasks
        that can be handled simultaneously.
    """
    if k <= 0 or m <= 0:
        raise ValueError("k (nodes per task) and m (max tasks per node) must be positive integers")
    if N <= 0:
        return 0

    workloads = N // k
    total_capacity = workloads * m

    return total_capacity

def determine_workload_distribution(nodes):
    """
    Determine the workload distribution among nodes.

    Args:
        nodes (np.ndarray): A NumPy array of integers where each integer represents a node.

    Returns:
        dict[int, int]: A dictionary with node IDs as keys and their corresponding workload count as values.
    """
    unique, counts = np.unique(nodes, return_counts=True)
    return dict(zip(unique, counts))

def distribute_tasks_randomly(nodes, num_tasks, k):
    """
    Distribute tasks randomly among nodes.

    Args:
        nodes (np.ndarray): A NumPy array representing the nodes and their current workloads.
        num_tasks (int): The number of tasks to distribute.
        k (int): The number of nodes to assign each task to.

    Returns:
        None: The function modifies the 'nodes' array in place.
    """
    N = len(nodes)
    task_assignments = np.random.randint(0, N, size=(num_tasks, k))
    np.add.at(nodes, task_assignments, 1)

def reduce_workload(nodes, m):
    """
    Reduce the workload of each node by m, ensuring no negative values.

    Args:
        nodes (np.ndarray): A NumPy array representing the nodes and their current workloads.
        m (int): The amount by which to reduce the workload of each node.

    Returns:
        None: The function modifies the 'nodes' array in place.
    """
    np.subtract(nodes, m, out=nodes)
    np.maximum(nodes, 0, out=nodes)

def run_frame(nodes, new_tasks, k, m, verbose=False):
    """
    Run a single frame of task distribution and workload reduction.

    Args:
        nodes (np.ndarray): A NumPy array representing the nodes and their current workloads.
        new_tasks (int): The number of new tasks to distribute.
        k (int): The number of nodes to assign each task to.
        m (int): The amount by which to reduce the workload of each node.
        verbose (bool): If True, print workload distributions before and after task distribution and reduction.

    Returns:
        None
    """
    if verbose:
        counter = determine_workload_distribution(nodes)
        print(counter)

    if new_tasks > 0:
        distribute_tasks_randomly(nodes, new_tasks, k)

    if verbose:
        counter = determine_workload_distribution(nodes)
        print(counter)

    reduce_workload(nodes, m)

    if verbose:
        counter = determine_workload_distribution(nodes)
        print(counter)

def simulate_task_distribution(N, k, m, t, f, c, verbose=False):
    """
    Simulates the distribution and execution of tasks across nodes in a network.
    
    Args:
        N (int): Number of nodes in the network.
        k (int): Number of nodes chosen per task.
        m (int): Maximum tasks a node can handle simultaneously.
        t (int): Time period (in seconds) for which tasks are executed.
        f (int): Number of frames of execution to run.
        c (float): Targeted network capacity.

    Returns:
        tuple: TPS (Transactions per second), time to clear (in frames), longest queue.
    """
    nodes = np.zeros(N, dtype=int)
    num_tasks = math.floor(estimate_network_capacity(N, k, m) * c)
    num_workloads = num_tasks * k
    num_workloads_over_frames = num_workloads * f

    if verbose:
        print(f"Number of tasks: {num_tasks}, workloads distributed: {num_workloads}")

    for _ in range(f):
        run_frame(nodes, num_tasks, k, m, verbose)

    counter = determine_workload_distribution(nodes)
    longest_queue = max(counter.keys())
    ttc = math.ceil(longest_queue / m) * t
    
    remaining_workloads = sum(key * counter[key] for key in counter.keys())

    if verbose:
        print(f"Remaining tasks after simulation: {remaining_workloads}")

    executed_tasks = num_workloads_over_frames - remaining_workloads
    tps = executed_tasks / k / f / t

    return (tps, ttc, longest_queue)

def main():
    parser = argparse.ArgumentParser(description="Simulate task distribution in a network of nodes.")
    
    parser.add_argument('-i', type=int, default=1, help='Number of iterations of the network simulation to run (default: 1)')
    parser.add_argument('-N', type=int, default=10000, help='Total number of nodes (default: 10000)')
    parser.add_argument('-k', type=int, default=3, help='Number of nodes chosen per task (default: 3)')
    parser.add_argument('-m', type=int, default=2, help='Simultaneous tasks per node (default: 2)')
    parser.add_argument('-t', type=int, default=1, help='Time per task (default: 1 second)')
    parser.add_argument('-f', type=int, default=1, help='Number of frames to run (default: 1)')
    parser.add_argument('-c', type=float, default=1.0, help='Targeted network capacity (default: 1.0)')
    parser.add_argument('-verbose', action='store_true', help='Add verbose logging (default: False)')
    
    args = parser.parse_args()

    print(f"Simulating with parameters: N={args.N}, k={args.k}, m={args.m}, t={args.t}, f={args.f}, c={args.c}; {args.i} times")
    
    totals = [0, 0, 0]
    for _ in range(args.i):
        tps, ttc, longest_queue = simulate_task_distribution(args.N, args.k, args.m, args.t, args.f, args.c, args.verbose)
        totals[0] += tps
        totals[1] += ttc
        totals[2] += longest_queue
    
    totals = [total / args.i for total in totals]
    
    print(f"[Averages] tps: {totals[0]}, ttc: {totals[1]}, longest queue: {totals[2]}")

if __name__ == "__main__":
    main()