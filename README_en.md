# A* Pathfinding Visualizer

This project is a visual and interactive implementation of the A* (A-star) algorithm in Python, allowing you to explore, learn, and experiment with pathfinding in 2D grids.

## Features

- Real-time animated visualization of the A* algorithm.
- Interactive graphical interface with PyQt5 (recommended).
- Place barriers, start, and goal points manually.
- Clear message when no path is possible.
- Step-by-step visualization of the algorithm (explored cells and frontier).
- Colorful, centered, and readable icon legend.
- Modern, centered interface.
- Quick restart of the configuration without closing the program.
- Clean, modular, and easy-to-understand code.

## How to Use

1. **Install dependencies:**

```bash
pip install numpy PyQt5
```

2. **Run the PyQt5 visualizer:**

```bash
python src/pyqt_visualizer.py
```

3. **Interface controls:**

- Click on the grid to add/remove barriers (default mode).
- Press `S` to select start mode and click to set the start point.
- Press `G` to select goal mode and click to set the goal.
- Press `B` to return to barrier mode.
- Press `Enter` or click "Rodar A*" to start pathfinding.
- If no path is possible, a message will be shown on the grid.
- After execution, press `R` or click "Resetar" to restart the configuration and try again.

## Project Structure

```
a_star_project/
├── src/
│   ├── a_star.py           # A* algorithm implementation
│   ├── pyqt_visualizer.py  # Main visualizer (PyQt5)
│   ├── utils.py            # Utility functions (cost, neighbors)
│   └── visualize.py        # Grid visualization and animation (Matplotlib, legacy)
├── tests/
│   └── test_a_star.py      # Unit tests
├── requirements.txt        # Project dependencies
└── README.md               # This file
```

## About the A* Algorithm

A* is an efficient heuristic search algorithm for finding the shortest path between two points in a graph or grid, widely used in games, robotics, and AI. It combines the actual path cost and a heuristic estimate (in this project, Manhattan distance).

## Heuristics in A*

A* uses a heuristic function to estimate the remaining cost to the goal. The choice of heuristic is crucial for efficiency and correctness:

- **Admissible heuristic:** never overestimates the true cost to the goal, ensuring A* finds the shortest path.
- **Consistent (monotonic) heuristic:** for every node n and neighbor n', the estimated cost from n to the goal is less than or equal to the cost to reach n' plus the estimate from n' to the goal.

### Why Manhattan?

This project uses Manhattan distance as the heuristic because:

- It is ideal for grids where movement is only allowed in four directions (up, down, left, right), as in this visualizer.
- It is simple, fast to compute, and always admissible and consistent in this context.
- It ensures A* finds the shortest path without exploring unnecessary paths.

If the grid allowed diagonal movement, other heuristics such as Euclidean distance might be more appropriate.

## Credits

Developed by Henrique Alonso.

---

Feel free to contribute, suggest improvements, or adapt for other grid types and heuristics!
