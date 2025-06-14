class AStar:
    def __init__(self, step_callback=None):
        self.open_set = set()
        self.closed_set = set()
        self.came_from = {}
        self.g_score = {}
        self.f_score = {}
        self.step_callback = step_callback

    def find_path(self, start, goal, grid=None):
        self.open_set = set([start])
        self.closed_set = set()
        self.came_from = {}
        self.g_score = {start: 0}
        self.f_score = {start: self.heuristic(start, goal)}

        while self.open_set:
            current = min(self.open_set, key=lambda x: self.f_score.get(x, float('inf')))
            if current == goal:
                return self.reconstruct_path(current)

            self.open_set.remove(current)
            self.closed_set.add(current)

            if self.step_callback:
                self.step_callback(current=current, open_set=self.open_set, closed_set=self.closed_set, came_from=self.came_from, grid=grid, start=start, goal=goal)

            for neighbor in self.get_neighbors(current):
                if neighbor in self.closed_set:
                    continue
                tentative_g_score = self.g_score[current] + self.cost(current, neighbor)
                if neighbor not in self.open_set:
                    self.open_set.add(neighbor)
                elif tentative_g_score >= self.g_score.get(neighbor, float('inf')):
                    continue
                self.came_from[neighbor] = current
                self.g_score[neighbor] = tentative_g_score
                self.f_score[neighbor] = self.g_score[neighbor] + self.heuristic(neighbor, goal)
        return None

    def heuristic(self, node1, node2): # Heurística (Manhattan)
        from utils import cost
        return cost(node1, node2)

    def reconstruct_path(self, current):
        total_path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def get_neighbors(self, node):
        from utils import get_neighbors
        return get_neighbors(node)

    def cost(self, node1, node2):
        from utils import cost
        return cost(node1, node2)