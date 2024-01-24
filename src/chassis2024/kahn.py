"""Kahn's Algorithm -- for Topological Sort

Given a list of edges, in the form:
  [(before, after), ...]

...return a sorting that makes every relationship true.


Code written by Chat-GPT, edited slightly by Lion Kimbro.
"""

from collections import defaultdict


CYCLE_DETECTED = "Cycle detected, topological sorting not possible."


def topological_sort(edges):
    # Create a dictionary to keep track of in-degrees of nodes
    in_degree = defaultdict(int)
    
    # Create a graph from the edges
    graph = defaultdict(list)
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Find all nodes with in-degree 0
    queue = [u for u in graph if in_degree[u] == 0]
    top_order = []

    while queue:
        node = queue.pop(0)
        top_order.append(node)

        # Reduce in-degree of adjacent nodes and add new 0 in-degree nodes to the queue
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if topological sorting is possible or not
    if len(top_order) == len(graph):
        return top_order
    else:
        return CYCLE_DETECTED

