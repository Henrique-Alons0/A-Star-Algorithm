def get_neighbors(node, grid=None):
    x, y = node
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if grid is None:
        for dx, dy in directions:
            neighbors.append((x + dx, y + dy))
        return neighbors
    rows, cols = len(grid), len(grid[0])
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def cost(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])