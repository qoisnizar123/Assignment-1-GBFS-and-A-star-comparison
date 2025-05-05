import heapq
import time

grid_str = [
    "S..#......",
    ".#.#.####.",
    ".#......#.",
    ".#####..#.",
    ".....#..#G",
    "####.#..##",
    "...#.#....",
    ".#.#.####.",
    ".#........",
    "....#####."
]

def parse_grid(grid):
    grid = [list(row) for row in grid]
    start = goal = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                start = (i, j)
            elif cell == "G":
                goal = (i, j)
    return grid, start, goal

def get_neighbors(pos, grid):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] != '#':
                neighbors.append((nx, ny))
    return neighbors

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    visited = set()
    pq = [(manhattan(start, goal), 0, start, [])]
    nodes = 0
    start_time = time.time()

    while pq:
        f, g, current, path = heapq.heappop(pq)
        if current == goal:
            return path + [current], time.time() - start_time, nodes
        if current in visited:
            continue
        visited.add(current)
        nodes += 1
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + manhattan(neighbor, goal)
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [current]))
    return None, time.time() - start_time, nodes

def print_grid(grid, path):
    grid_copy = [row[:] for row in grid]
    for x, y in path:
        if grid_copy[x][y] not in "SG":
            grid_copy[x][y] = "*"
    for row in grid_copy:
        print("".join(row))

grid, start, goal = parse_grid(grid_str)
path, exec_time, nodes = astar(grid, start, goal)
print_grid(grid, path)
print(f"\n[A*] Steps: {len(path)-1}, Time: {exec_time:.4f}s, Nodes explored: {nodes}")