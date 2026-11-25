---
name: algo-bfs-dfs
description: "BFS (queue) and DFS (stack/recursion) traversal in pure Python for shortest unweighted path, k-hop neighborhood, connected components, cycle detection on PPI/regulatory networks. Use for shortest path or cycle detection."
tool_type: python
primary_tool: collections.deque
---

# Graph Traversals: BFS and DFS

## When to Use
- Finding the shortest path between two genes/proteins in an unweighted interaction network.
- Enumerating all nodes reachable within k hops of a seed node (network neighborhood).
- Splitting a network into connected components / functional modules.
- Detecting cycles (e.g., feedback loops in a regulatory graph).
- Level-order traversal or general reachability queries on any graph, tree, or state space.

## Version Compatibility
Pure Python standard library only — no version sensitivity. Examples use Python ≥3.8 (`collections.deque`, `defaultdict`). Optional visualization uses matplotlib ≥3.5 or networkx ≥3.0 if you want to plot the graph instead of building the adjacency list by hand.

## Prerequisites
- Comfort with adjacency-list graph representation (see `algo-graph-representations`).
- Core data structures: queue (FIFO) for BFS, stack (LIFO)/recursion for DFS — see `algo-stacks-queues`.
- No external packages required; `from collections import defaultdict, deque` covers everything below.

**Goal:** represent a graph and traverse it two ways — level-by-level (BFS) or branch-by-branch (DFS) — each in O(V + E) time.

**Approach:** back every traversal with a plain adjacency-list `Graph`, use a `deque` for BFS's queue and a list-as-stack (or recursion) for DFS, and track a `visited` set so each vertex is processed once.

```python
from collections import defaultdict, deque


class Graph:
    """Simple undirected graph using an adjacency list (set per vertex)."""

    def __init__(self):
        self.adj = defaultdict(set)

    def add_edge(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def neighbors(self, v):
        return self.adj[v]

    def vertices(self):
        return list(self.adj.keys())


def bfs(graph, start):
    """
    Breadth-First Search from start vertex.
    Returns: (visited order, distances from start)
    Time: O(V + E), Space: O(V)
    """
    visited = {start}
    queue = deque([start])
    order = []
    distances = {start: 0}

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                distances[neighbor] = distances[vertex] + 1

    return order, distances


def find_neighbors_within_k(graph, start, k):
    """Find all vertices within k edges of start (network neighborhood)."""
    _, distances = bfs(graph, start)
    return [v for v, d in distances.items() if d <= k and v != start]


# Build a sample PPI network
ppi = Graph()
edges = [
    ('TP53', 'MDM2'), ('TP53', 'BRCA1'), ('TP53', 'ATM'),
    ('MDM2', 'RB1'), ('BRCA1', 'CHEK2'), ('ATM', 'CHEK2'),
    ('RB1', 'E2F1'), ('CHEK2', 'CDC25A'),
]
for u, v in edges:
    ppi.add_edge(u, v)

order, distances = bfs(ppi, 'TP53')
print("BFS traversal from TP53:", order)
neighborhood = find_neighbors_within_k(ppi, 'TP53', 2)
print(f"Genes within 2 hops of TP53: {neighborhood}")
```

**Goal:** explore a graph depth-first (iterative or recursive) and use it to split a network into connected components.

**Approach:** DFS with an explicit stack avoids Python recursion-depth limits on large graphs; the recursive version is shorter and fine for small networks. Reuse the same stack-based pattern to peel off one connected component at a time.

```python
def dfs_iterative(graph, start):
    """Depth-First Search using an explicit stack. Time: O(V+E), Space: O(V)."""
    visited = set()
    stack = [start]
    order = []

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)
            for neighbor in sorted(graph.neighbors(vertex), reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)

    return order


def dfs_recursive(graph, start, visited=None):
    """DFS using recursion. Not safe for very deep/large graphs (stack limit)."""
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbor in sorted(graph.neighbors(start)):
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))
    return order


def find_connected_components(graph):
    """Find all connected components using DFS (functional modules/pathways)."""
    visited = set()
    components = []

    for vertex in graph.vertices():
        if vertex not in visited:
            component = []
            stack = [vertex]
            while stack:
                v = stack.pop()
                if v not in visited:
                    visited.add(v)
                    component.append(v)
                    for neighbor in graph.neighbors(v):
                        if neighbor not in visited:
                            stack.append(neighbor)
            components.append(component)

    return components


print("DFS iterative from TP53:", dfs_iterative(ppi, 'TP53'))
print("DFS recursive from TP53:", dfs_recursive(ppi, 'TP53'))

# Add a disconnected component and re-check
ppi.add_edge('KRAS', 'BRAF')
ppi.add_edge('BRAF', 'MEK1')
components = find_connected_components(ppi)
print(f"Found {len(components)} connected components:")
for i, comp in enumerate(components, 1):
    print(f"  Component {i}: {comp}")
```

**Goal:** find the shortest path between two specific nodes, and detect whether an undirected graph has a cycle (feedback loop).

**Approach:** track the path alongside each queued vertex for BFS shortest-path reconstruction; for cycle detection, DFS with a `parent` pointer so a "back edge" to anything other than the immediate parent means a cycle.

```python
def shortest_path(graph, start, end):
    """Find shortest path from start to end using BFS (unweighted graph)."""
    if start == end:
        return [start]

    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        vertex, path = queue.popleft()
        for neighbor in graph.neighbors(vertex):
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path exists


def has_cycle(graph):
    """Detect if an undirected graph has a cycle using DFS."""
    visited = set()

    def dfs(vertex, parent):
        visited.add(vertex)
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                if dfs(neighbor, vertex):
                    return True
            elif neighbor != parent:
                return True  # back edge to a non-parent -> cycle
        return False

    for v in graph.vertices():
        if v not in visited:
            if dfs(v, None):
                return True
    return False


path = shortest_path(ppi, 'E2F1', 'ATM')
print(f"Shortest path E2F1 -> ATM: {' -> '.join(path)}")

ppi.add_edge('ATM', 'BRCA1')  # creates TP53-ATM-BRCA1-TP53 cycle
print(f"Network has cycle: {has_cycle(ppi)}")
```

## BFS vs DFS Comparison

| Feature | BFS | DFS |
|---------|-----|-----|
| Data structure | Queue | Stack/Recursion |
| Explores | Level by level | Branch by branch |
| Shortest path (unweighted) | Yes | No |
| Memory | O(width) | O(depth) |
| Cycle detection | Possible | Natural fit |
| Topological sort | No | Yes |

## Pitfalls
- **Undirected cycle check needs the parent pointer.** Without excluding the edge back to the immediate parent, `has_cycle` reports a false cycle on every simple edge (A-B looks like it revisits A).
- **Recursive DFS hits Python's recursion limit** (~1000 by default) on long chains/large graphs — use `dfs_iterative` or raise `sys.setrecursionlimit` deliberately.
- **BFS with a plain `visited` check but no distance/path tracking** loses the very information (hop count, path) you usually want — always update `distances`/`path` at the moment a neighbor is first discovered, not later.
- **Weighted graphs**: BFS shortest path only works when all edges have equal weight; for weighted edges use Dijkstra instead (`algo-dijkstra`).
- **Directed vs undirected**: `Graph.add_edge` here is undirected (adds both directions); for directed graphs (e.g., regulatory "A activates B") don't add the reverse edge, and note that cycle detection/topological sort logic differs.

## See Also
- `algo-graph-representations` — adjacency list/matrix construction and trade-offs.
- `algo-dijkstra` — shortest paths on weighted graphs.
- `algo-topological-sort` — DFS-based ordering for DAGs (regulatory/pathway graphs).
- `algo-mst-kruskal-prim` — minimum spanning trees built on similar traversal ideas.
