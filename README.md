### README.md

# Network Task Distribution Simulator (Random Assignment)

A network simulator to experimentally verify workload distribution and load characteristics in an environment lacking orchestrators or communication strategies (such as a gossip protocol) between nodes; instead, all task assignments are random.

Quantities of tasks are not explicitly declared; instead, the capacity is inferred from the total number of nodes in the network, the number of nodes required for replication, and the number of workloads each node can handle.

A frame represents adding a full set of workloads to all the nodes (according to the capacity modifier) and then simulating the reduction in the nodes' queues after completing the tasks. Time of execution is constant according to a user defined variable. This allows the user to play the network state forward under a constant load and discover bottlenecks and failure points.

We take our inspiration from fluid limit models in queuing systems and expect that over many frames the law of large numbers will evenly distribute the workload over all nodes. Further, that when the network is operating efficiently the queue length will grow logarithmically and approach an asymptote - converging towards steady-state performance - or, when overloaded, the queue length will grow exponentially.[1]

The entire simulation (including execution of frames) can be re-run multiple times and have their results averaged in order to fine tune behavior.

### Key Concepts

1. **Tasks and Workloads**:
   - **Tasks**: Units of work to be performed, which can be replicated or split across multiple nodes.
   - **Workloads**: Assignments given to nodes, derived from tasks.
   - **Frames**: A window of time in which all nodes receive new tasks, and one pass of execution is performed across all queues.
   - **Iterations**: Separate simulations (re-running starting state and all frames) with the results averaged together.

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
   - `ttc`: time to clear the queue (divide by `t` and `m`)
   - `longest queue`: number of outstanding workloads assigned to some node(s)

### Simulation Behavior

- **Logarithmic Growth**: At capacities below a critical point, the network operates efficiently, and queue lengths grow logarithmically, approaching an asymptote.
- **Exponential Growth**: At capacities at a critical point and above, the network becomes overloaded, and queue lengths grow exponentially, indicating significant performance degradation.

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

### Example Statistics for Longest Queue with N=10000, k=1, m=1, t=1

| Iterations | Frames | 0.1     | 0.2     | 0.3     | 0.4     | 0.5     | 0.6     | 0.7     | 0.8     | 0.9     | 1       | 1.1     | 1.2     | 1.3     | 1.4     | 1.5     |
|------------|--------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| 1000000    | 1      | 1.826688| 2.45605 | 3.08449 | 3.499765| 3.963814| 4.33715 | 4.686332| 5.051388| 5.37283 | 5.67281 | 5.983549| 6.28206 | 6.55742 | 6.828485| 7.103409|
| 100000     | 10     | 1.93292 | 2.87534 | 3.91021 | 5.14741 | 6.56882 | 8.10276 | 9.69372 | 11.28625| 12.88171| 14.46261| 16.02698| 17.57259| 19.10822| 20.60626| 22.10989|
| 10000      | 100    | 1.94    | 2.8727  | 3.9016  | 5.2184  | 6.9603  | 9.4915  | 13.6447 | 20.7832 | 30.8383 | 41.9701 | 53.4568 | 65.0389 | 76.5826 | 88.1943 | 99.727  |
| 1000       | 1000   | 1.933   | 2.843   | 3.909   | 5.234   | 6.92    | 9.515   | 13.717  | 21.874  | 46.148  | 128.72  | 232.294 | 336.704 | 442.24  | 546.759 | 652.077 |
| 100        | 10000  | 1.88    | 2.91    | 4.01    | 5.28    | 7.11    | 9.57    | 13.82   | 22.09   | 46.13   | 405.43  | 1409.5  | 2427.92 | 3443.86 | 4464.99 | 5473.49 |
| 10         | 100000 | 2       | 3       | 4.4     | 5.3     | 6.9     | 9.9     | 13.6    | 22      | 46.4    | 1245.4  | 11230.2 | 21277.2 | 31335.5 | 41344.4 | 51454   |
| 1          | 1000000| 2       | 3       | 3       | 6       | 6       | 12      | 13      | 18      | 46      | 4448    | 104228  | 204804  | 305014  | 404945  | 505175  |


## Interpretation of Results

The results will indicate the average performance metrics over the specified iterations, such as tasks per second (TPS), time to clear tasks (TTC), and the longest queue. The following trends are typically observed:

- **Iterations**: More iterations result in finer-tuned averages; the time required to calculate 1 frame 1,000,000 times is about the same as 1,000,000 continuous frames a single time.
- **Capacities < 0.9**: Network operates efficiently with manageable queue lengths under one minute.
- **Capacities ≥ 0.9**: Network becomes overloaded, leading to exponential growth in queue lengths and significant delays.

## Citations

1. J. G. Dai and S. P. Meyn, "Stability and convergence of moments for multiclass queueing networks via fluid limit models," IEEE Transactions on Automatic Control, vol. 40, no. 11, pp. 1889-1904, Nov. 1995, doi: 10.1109/9.471210.

## AI Attribution

This content was generated in whole or part with the assistance of an AI model - see the [AI.md](AI.md) file for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.