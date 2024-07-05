### README.md

# Network Task Distribution Simulator (Random Assignment)

A network simulator designed for emulating random assignment of tasks under varying load conditions. The simulator allows for replicated workloads and nodes capable of handling multiple simultaneous jobs. Execution times for each task are constant for simplicity.

Frames can be executed one after another to simulate a constant load over time to discover bottlenecks and failure points, and the simulation can be re-run over multiple iterations to average the results from each.

This simulator demonstrates workload distirbution in an environment lacking orchestrators or communication strategies (such as a gossip protocol) between nodes.

### Key Concepts

1. **Tasks and Workloads**:
   - **Tasks**: Units of work to be performed, which can be replicated across multiple nodes.
   - **Workloads**: Assignments given to nodes, derived from tasks.

2. **Parameters**:
   - `N`: Total number of nodes in the network.
   - `k`: Number of nodes required to handle each task (replication factor).
   - `m`: Maximum number of workloads a single node can handle simultaneously.
   - `t`: Time per workload (constant).
   - `f`: Number of consecutive frames to run.
   - `c`: Targeted network capacity as a fraction of the estimated capacity.
   - `i`: Number of iterations to run (results are averaged)

3. **Outputs**:
   - `tps`: tasks per second
   - `ttc`: time to clear the queue
   - `longest queue`: number of outstanding workloads assigned to some node(s) (divide by `t` and `m` to get `ttc`)

### Simulation Behavior

- **Logarithmic Growth**: At capacities below approximately 0.9, the network operates efficiently, and queue lengths grow logarithmically, approaching an asymptote.
- **Exponential Growth**: At capacities of 0.9 and above, the network becomes overloaded, and queue lengths grow exponentially, indicating significant performance degradation.

## Installation

### Prerequisites

- Python 3.x
- `numpy` library

### Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/tcotten-scrypted/network-simulator-random-assignment.git
   ```
2. Navigate to the project directory:
   ```sh
   cd network-simulator-random-assignment
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running the Simulation

To run the simulation, use the following command:

```bash
python simulator.py -N <nodes> -k <replication_factor> -m <max_tasks_per_node> -t <time_per_task> -f <frames> -c <capacity> [-i <iterations>] [--verbose]
```

### Command-Line Arguments

- `-N`: Total number of nodes (default: 10000)
- `-k`: Number of nodes chosen per task (default: 3)
- `-m`: Simultaneous tasks per node (default: 2)
- `-t`: Time per task in seconds (default: 1)
- `-f`: Number of frames to run (default: 1)
- `-c`: Targeted network capacity (default: 1.0)
- `-i`: Number of iterations of the network simulation to run (default: 1)
- `--verbose`: Enable verbose logging

### Example Usage

```bash
python simulator.py
```

Expected output:

```bash
Simulating with parameters: N=10000, k=3, m=2, t=1, f=1, c=1.0; 1 times
[Averages] tps: 4858.666666666667, ttc: 4.0, longest queue: 8.0
```

### Example Statistics for Longest Queue with -k 1 -m 1 -t 1

| Iterations | Frames | 0.1   | 0.2   | 0.3   | 0.4   | 0.5   | 0.6   | 0.7   | 0.8   | 0.9   | 1     | 1.1   | 1.2   | 1.3   | 1.4   | 1.5   |
|------------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| 100000     | 1      | 1.82868 | 2.45935 | 3.08634 | 3.4992  | 3.96684 | 4.34215 | 4.68371 | 4.68371 | 5.37245 | 5.67292 | 5.67292 | 6.2806  | 6.55972 | 6.82958 | 7.10605 |
| 10000      | 10     | 1.939 | 2.8736 | 3.916 | 5.1331 | 6.5598 | 8.1015 | 9.6878 | 11.2829 | 12.8801 | 14.4542 | 16.0203 | 17.5714 | 19.1284 | 20.6254 | 22.1094 |
| 1000       | 100    | 1.932 | 2.88 | 3.894 | 5.159 | 6.923 | 9.448 | 13.538 | 20.8 | 30.845 | 41.943 | 53.408 | 64.941 | 76.49 | 88.097 | 99.727 |
| 100        | 1000   | 1.91 | 2.91 | 3.91 | 5.07 | 6.82 | 9.57 | 13.56 | 21.68 | 47.76 | 130.42 | 233.58 | 337.22 | 442.25 | 548.13 | 652.48 |
| 10         | 10000  | 2 | 3.1 | 4.3 | 5.3 | 7.4 | 9.4 | 13.1 | 20.9 | 51.3 | 401.8 | 1407.8 | 2431.1 | 3431.1 | 4466.7 | 5470 |
| 1          | 100000 | 2 | 3 | 6 | 5 | 6 | 10 | 13 | 23 | 54 | 1250 | 11148 | 21280 | 31469 | 41342 | 51397 |
| 1          | 1000000| 2 | 3 | 3 | 6 | 6 | 12 | 13 | 18 | 46 | 4448 | 104228 | 204804 | 305014 | 404945 | 505175 |

## Interpretation of Results

The results will indicate the average performance metrics over the specified iterations, such as tasks per second (TPS), time to clear tasks (TTC), and the longest queue. The following trends are typically observed:

- **Capacities < 0.9**: Network operates efficiently with manageable queue lengths.
- **Capacities ≥ 0.9**: Network becomes overloaded, leading to exponential growth in queue lengths and significant delays.

## Understanding the Simulation Code

The core functions of the simulator include:

- `estimate_network_capacity`: Estimates the total network capacity.
- `determine_workload_distribution`: Determines the workload distribution among nodes.
- `distribute_tasks_randomly`: Distributes tasks randomly across nodes.
- `reduce_workload`: Reduces the workload on each node.
- `run_frame`: Executes a single frame of task distribution and workload reduction.
- `simulate_task_distribution`: Runs the full simulation and calculates performance metrics.

The difference between frames and iterations:
- frames represent a new aggregate workload added to the network (based on the specified capacity) after a reduction in completed tasks
- iterations repeat the entire simulation and average the results

## AI Attribution

This content was generated in whole or part with the assistance of an AI model - see the [AI.md](AI.md) file for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.