from src.a_star import AStar
import unittest
from src.utils import get_neighbors, cost
import numpy as np

class TestAStar(unittest.TestCase):

    def setUp(self):
        self.astar = AStar()

    def test_find_path(self):
        start = (0, 0)
        goal = (1, 1)
        path = self.astar.find_path(start, goal)
        expected_path = [(0, 0), (0, 1), (1, 1)]  # Example expected path
        self.assertEqual(path, expected_path)

    def test_simple_path(self):
        start = (0, 0)
        goal = (1, 1)
        self.astar.get_neighbors = lambda node: get_neighbors(node, np.zeros((2,2), dtype=int))
        path = self.astar.find_path(start, goal)
        self.assertIn(goal, path)
        self.assertEqual(path[0], start)

    def test_no_path(self):
        grid = np.zeros((3,3), dtype=int)
        grid[1,0] = 1
        grid[1,1] = 1
        grid[1,2] = 1
        self.astar.get_neighbors = lambda node: get_neighbors(node, grid)
        path = self.astar.find_path((0,0), (2,2))
        self.assertIsNone(path)

    def test_cost(self):
        self.assertEqual(cost((0,0), (1,1)), 2)
        self.assertEqual(cost((2,2), (2,2)), 0)

    def test_heuristic(self):
        node1 = (0, 0)
        node2 = (1, 1)
        heuristic_cost = self.astar.heuristic(node1, node2)
        expected_cost = 2
        self.assertEqual(heuristic_cost, expected_cost)

        self.assertEqual(self.astar.heuristic((0,0), (2,2)), 4)
        self.assertEqual(self.astar.heuristic((1,1), (1,1)), 0)

    def test_grid_with_obstacles(self):
        grid = np.zeros((5,5), dtype=int)
        grid[2,1:4] = 1
        self.astar.get_neighbors = lambda node: get_neighbors(node, grid)
        path = self.astar.find_path((0,0), (4,4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0,0))
        self.assertEqual(path[-1], (4,4))

if __name__ == '__main__':
    unittest.main()