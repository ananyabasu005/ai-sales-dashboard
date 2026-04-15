from models.regression import predict_sales
from algorithms.bfs_dfs import bfs, dfs
from algorithms.dijkstra import dijkstra

print("=== SALES FORECASTING ===")
predict_sales()

print("\n=== BFS DFS ===")
bfs('A')
print("DFS:", dfs('A'))

print("\n=== DIJKSTRA ===")
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 2, 'D': 5},
    'C': {'D': 1},
    'D': {}
}
print(dijkstra(graph, 'A'))