graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': [],
    'E': []
}

def bfs(start):
    visited = []
    queue = [start]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            queue.extend(graph[node])

    print("BFS:", visited)

def dfs(node, visited=None):
    if visited is None:
        visited = []

    visited.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)

    return visited