import heapq
import math
from collections import deque

class PipeNetwork:
    def __init__(self, junctions, pipes, start, target):
        self.junctions = junctions  # Dictionary: junction_id -> (x, y)
        self.pipes = pipes          # List of (junction1, junction2, cost)
        self.start = start
        self.target = target
        self.graph = self.build_graph()
    
    def build_graph(self):
        """Build adjacency list representation of the pipe network"""
        graph = {}
        for junction in self.junctions:
            graph[junction] = []
        
        for j1, j2, cost in self.pipes:
            graph[j1].append((j2, cost))
            graph[j2].append((j1, cost))  # Assuming bidirectional pipes
        
        return graph
    
    def heuristic(self, junction1, junction2):
        """Calculate straight-line distance between two junctions"""
        x1, y1 = self.junctions[junction1]
        x2, y2 = self.junctions[junction2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def dfs_path(self):
        """Depth-First Search - Go deeper into unexplored pipes first"""
        visited = set()
        path = []
        total_cost = 0
        junctions_visited = 0
        
        def dfs_recursive(current, current_path, current_cost):
            nonlocal path, total_cost, junctions_visited
            
            visited.add(current)
            current_path.append(current)
            junctions_visited += 1
            
            if current == self.target:
                path = current_path.copy()
                total_cost = current_cost
                return True
            
            # Sort neighbors to ensure consistent behavior (go to higher numbered junctions first for depth)
            neighbors = sorted(self.graph[current], key=lambda x: x[0], reverse=True)
            
            for neighbor, cost in neighbors:
                if neighbor not in visited:
                    if dfs_recursive(neighbor, current_path, current_cost + cost):
                        return True
            
            current_path.pop()
            return False
        
        dfs_recursive(self.start, [], 0)
        return path, total_cost, junctions_visited
    
    def bfs_path(self):
        """Breadth-First Search - Check all nearby pipes before moving deeper"""
        queue = deque([(self.start, [self.start], 0)])
        visited = set([self.start])
        junctions_visited = 0
        
        while queue:
            current, path, cost = queue.popleft()
            junctions_visited += 1
            
            if current == self.target:
                return path, cost, junctions_visited
            
            # Sort neighbors to ensure consistent exploration order
            neighbors = sorted(self.graph[current], key=lambda x: x[0])
            
            for neighbor, pipe_cost in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    new_cost = cost + pipe_cost
                    queue.append((neighbor, new_path, new_cost))
        
        return [], 0, junctions_visited
    
    def dijkstra_path(self):
        """Dijkstra's Algorithm - Find the path with lowest total travel cost"""
        distances = {junction: float('inf') for junction in self.junctions}
        distances[self.start] = 0
        previous = {}
        pq = [(0, self.start)]
        visited = set()
        junctions_visited = 0
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            junctions_visited += 1
            
            if current == self.target:
                break
            
            for neighbor, cost in self.graph[current]:
                distance = current_dist + cost
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = self.target
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        return path, distances[self.target], junctions_visited
    
    def astar_path(self):
        """A* Algorithm - Use heuristic to guide search toward target"""
        open_set = [(0, self.start)]
        came_from = {}
        g_score = {junction: float('inf') for junction in self.junctions}
        g_score[self.start] = 0
        f_score = {junction: float('inf') for junction in self.junctions}
        f_score[self.start] = self.heuristic(self.start, self.target)
        junctions_visited = 0
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            junctions_visited += 1
            
            if current == self.target:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start)
                path.reverse()
                return path, g_score[self.target], junctions_visited
            
            for neighbor, cost in self.graph[current]:
                tentative_g = g_score[current] + cost
                
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, self.target)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return [], 0, junctions_visited

def run_simulation():
    """Example usage with sample data"""
    # Sample pipe network (you'll replace this with your actual data)
    junctions = {
        'A': (0, 0),    # Starting junction
        'B': (3, 4),
        'C': (8, 2),
        'D': (5, 8),
        'E': (10, 6),   # Target junction (cheese location)
    }
    
    pipes = [
        ('A', 'B', 5),
        ('A', 'C', 10),
        ('B', 'C', 3),
        ('B', 'D', 7),
        ('C', 'E', 4),
        ('D', 'E', 2),
    ]
    
    network = PipeNetwork(junctions, pipes, 'A', 'E')
    
    print("=== TERRY'S PIPE ESCAPE RESULTS ===\n")
    
    # Strategy 1: Depth-First Search
    dfs_path, dfs_cost, dfs_visited = network.dfs_path()
    print("1. DEPTH-FIRST SEARCH (Go deeper first):")
    print(f"   Path: {' -> '.join(dfs_path)}")
    print(f"   Total Cost: {dfs_cost}")
    print(f"   Junctions Visited: {dfs_visited}\n")
    
    # Strategy 2: Breadth-First Search
    bfs_path, bfs_cost, bfs_visited = network.bfs_path()
    print("2. BREADTH-FIRST SEARCH (Check nearby pipes first):")
    print(f"   Path: {' -> '.join(bfs_path)}")
    print(f"   Total Cost: {bfs_cost}")
    print(f"   Junctions Visited: {bfs_visited}\n")
    
    # Strategy 3: Dijkstra's Algorithm
    dijkstra_path, dijkstra_cost, dijkstra_visited = network.dijkstra_path()
    print("3. DIJKSTRA'S ALGORITHM (Lowest cost path):")
    print(f"   Path: {' -> '.join(dijkstra_path)}")
    print(f"   Total Cost: {dijkstra_cost}")
    print(f"   Junctions Visited: {dijkstra_visited}\n")
    
    # Strategy 4: A* Algorithm
    astar_path, astar_cost, astar_visited = network.astar_path()
    print("4. A* ALGORITHM (Using straight-line distance heuristic):")
    print(f"   Path: {' -> '.join(astar_path)}")
    print(f"   Total Cost: {astar_cost}")
    print(f"   Junctions Visited: {astar_visited}\n")
    
    print("=== COMPARISON ===")
    strategies = [
        ("DFS", dfs_cost, dfs_visited),
        ("BFS", bfs_cost, bfs_visited), 
        ("Dijkstra", dijkstra_cost, dijkstra_visited),
        ("A*", astar_cost, astar_visited)
    ]
    
    print("Strategy    | Cost | Junctions Visited")
    print("------------|------|------------------")
    for name, cost, visited in strategies:
        print(f"{name:<11} | {cost:<4} | {visited}")

if __name__ == "__main__":
    run_simulation()
