def astar(graph, start, goal, heuristic):
    open_list = [(0, start)]
    g = {start: 0}

    while open_list:
        open_list.sort()
        cost, node = open_list.pop(0)

        if node == goal:
            return g[node]

        for neighbor, weight in graph[node].items():
            new_cost = g[node] + weight
            if neighbor not in g or new_cost < g[neighbor]:
                g[neighbor] = new_cost
                f = new_cost + heuristic[neighbor]
                open_list.append((f, neighbor))