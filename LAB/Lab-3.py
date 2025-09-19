import math
import heapq

# Custom Euclidean heuristic
def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Heuristic options: Manhattan, Euclidean, Diagonal
def get_heuristic(a, b, method):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    if method == "manhattan":
        return dx + dy
    if method == "euclidean":
        return euclidean(a, b)
    if method == "diagonal":
        return max(dx, dy)
    return 0

def setup_grid(grid_str):
    grid = [list(row) for row in grid_str.strip().split('/')]
    start = goal = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                start = (i, j)
            elif cell == "G":
                goal = (i, j)
    return grid, start, goal

def neighbors(pos, grid):
    moves = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]
    res = []
    for dx, dy in moves:
        x, y = pos[0]+dx, pos[1]+dy
        if 0<=x<len(grid) and 0<=y<len(grid[0]) and grid[x][y] != '1':
            res.append((x,y))
    return res

def step_cost(current, neighbor, grid):
    x, y = neighbor
    if grid[x][y] == '6':  # Ghost zone
        return 6
    # Diagonal step is cost sqrt(2), else 1
    if abs(current[0]-neighbor[0]) + abs(current[1]-neighbor[1]) == 2:
        return math.sqrt(2)
    return 1

def retrace(came_from, end, start):
    if end not in came_from:
        return []
    path = []
    curr = end
    while curr != start:
        path.append(curr)
        curr = came_from[curr]
    path.append(start)
    return path[::-1]

def greedy(grid, start, goal, method):
    queue = []
    heapq.heappush(queue, (get_heuristic(start, goal, method), start))
    came_from = {start: None}
    explored = set()
    while queue:
        _, pos = heapq.heappop(queue)
        if pos == goal:
            break
        explored.add(pos)
        for neigh in neighbors(pos, grid):
            if neigh not in came_from:
                heapq.heappush(queue, (get_heuristic(neigh, goal, method), neigh))
                came_from[neigh] = pos
    path = retrace(came_from, goal, start)
    return path, len(explored)

def astar(grid, start, goal, method):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = set()
    while queue:
        _, pos = heapq.heappop(queue)
        if pos == goal:
            break
        explored.add(pos)
        for neigh in neighbors(pos, grid):
            cost = cost_so_far[pos] + step_cost(pos, neigh, grid)
            if neigh not in cost_so_far or cost < cost_so_far[neigh]:
                cost_so_far[neigh] = cost
                priority = cost + get_heuristic(neigh, goal, method)
                heapq.heappush(queue, (priority, neigh))
                came_from[neigh] = pos
    path = retrace(came_from, goal, start)
    return path, len(explored)

def print_path(grid, path):
    view = [row[:] for row in grid]
    for x, y in path:
        if view[x][y] not in ('S','G'):
            view[x][y] = '*'
    for row in view:
        print(''.join(row))
    print()

def main(grid_str):
    grid, start, goal = setup_grid(grid_str)
    heuristics = ["manhattan", "euclidean", "diagonal"]
    for h in heuristics:
        print(f"Greedy ({h})")
        path, nodes = greedy(grid, start, goal, h)
        print(f"Path: {len(path)} Nodes Explored: {nodes}")
        print_path(grid, path)
        print(f"A* ({h})")
        path, nodes = astar(grid, start, goal, h)
        print(f"Path: {len(path)} Nodes Explored: {nodes}")
        print_path(grid, path)

main("S0000/10101/06010/10101/0000G")
