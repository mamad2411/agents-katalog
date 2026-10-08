---
name: algo-dijkstra
description: Compute single-source shortest paths in a non-negative-weight graph with Dijkstra's algorithm (binary-heap priority queue, O((V+E) log V)); reconstruct paths and find network diameter. Use when finding shortest/cheapest/most-reliable path, routing, weighted PPI/interaction-network distance, or ranking paths by confidence score product.
tool_type: python
primary_tool: Python
---

# Dijkstra's Algorithm: Shortest Paths in Weighted Graphs

## When to Use

- Finding the shortest or lowest-cost path between two nodes in a graph with non-negative edge weights (routing, network latency, cost minimization).
- Computing distances from one source to every other node (e.g. "how far is every gene from TP53 in a confidence-weighted PPI network?").
- Ranking candidate paths by a multiplicative score (reliability, probability) by converting products to sums via `-log`.
- Computing graph diameter / eccentricity by running Dijkstra from every vertex.
- Any request mentioning "shortest path", "weighted graph", "priority queue graph search", or "min-heap graph traversal" — do NOT use this if any edge weight can be negative (use Bellman-Ford instead).

## Version Compatibility

Pure Python standard library — `heapq` and `collections.defaultdict`. Works on Python ≥3.8 (uses f-strings and dict ordering guarantees); no third-party dependencies.

## Prerequisites

- Comfortable with graph representations (adjacency list) — see `algo-graph-representations`.
- Familiarity with BFS/DFS traversal order — see `algo-bfs-dfs`.
- `import heapq` and `from collections import defaultdict` (both stdlib).

## Core Algorithm

**Goal:** Find the shortest distance (and the path) from a single source vertex to every reachable vertex in a weighted graph with non-negative edge weights.

**Approach:** Greedily pop the vertex with the smallest tentative distance from a min-heap, mark it final, and relax its outgoing edges. Once a vertex is popped, its distance can never improve again — this invariant is what makes the greedy approach correct, and it only holds when all weights are ≥ 0.

```python
import heapq
import math
from collections import defaultdict


class WeightedGraph:
    """Weighted graph using an adjacency list."""

    def __init__(self):
        self.adj = defaultdict(list)  # vertex -> [(neighbor, weight), ...]

    def add_edge(self, u, v, weight, directed=False):
        self.adj[u].append((v, weight))
        if not directed:
            self.adj[v].append((u, weight))

    def vertices(self):
        return list(self.adj.keys())


def dijkstra(graph, start):
    """
    Dijkstra's algorithm using a min-heap.

    Works for both undirected and directed graphs, including directed
    graphs where some vertices only appear as edge targets (no outgoing
    edges) — those are discovered lazily via distances.get().

    Time complexity: O((V + E) log V) with a binary heap
    Space complexity: O(V)

    Parameters
    ----------
    graph : WeightedGraph
        Weighted graph with non-negative edge weights.
    start : hashable
        Source vertex.

    Returns
    -------
    distances : dict
        Shortest distance from start to every reachable vertex.
    predecessors : dict
        predecessors[v] = vertex immediately before v on the shortest
        path from start. Used by reconstruct_path().
    """
    distances = {v: float('inf') for v in graph.vertices()}
    distances[start] = 0
    predecessors = {start: None}

    heap = [(0, start)]  # (tentative_distance, vertex)
    visited = set()

    while heap:
        dist, u = heapq.heappop(heap)
        if u in visited:  # stale entry, a cheaper path already finalized u
            continue
        visited.add(u)

        for v, weight in graph.adj[u]:
            if v in visited:
                continue
            new_dist = dist + weight
            if new_dist < distances.get(v, float('inf')):
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, predecessors


def reconstruct_path(predecessors, end):
    """Reconstruct the shortest path from a predecessors dict.

    Returns an ordered list of vertices from source to `end`, or an
    empty list if `end` is unreachable.
    """
    if end not in predecessors:
        return []
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors.get(current)
    return path[::-1]
```

## Applied Example: Confidence-Weighted PPI Network

**Goal:** Given a protein-protein interaction network where edges carry a confidence score (0-1, higher = more confident), find the shortest-distance paths from a source protein, treating higher confidence as lower "distance".

**Approach:** Convert each confidence score to a distance with `1 - confidence` before adding the edge, then run `dijkstra` unchanged.

```python
# Build weighted PPI network (weights = interaction confidence)
# Lower weight = higher confidence (we minimize distance)
ppi = WeightedGraph()
interactions = [
    ('TP53', 'MDM2', 0.01),   # very high confidence
    ('TP53', 'BRCA1', 0.15),
    ('TP53', 'ATM', 0.08),
    ('MDM2', 'RB1', 0.20),
    ('BRCA1', 'CHEK2', 0.12),
    ('ATM', 'CHEK2', 0.05),
    ('RB1', 'E2F1', 0.10),
    ('CHEK2', 'CDC25A', 0.18),
]

for u, v, conf in interactions:
    # Convert confidence to distance: higher confidence = lower weight
    ppi.add_edge(u, v, 1 - conf)

distances, predecessors = dijkstra(ppi, 'TP53')

print("Shortest path distances from TP53:")
for gene, dist in sorted(distances.items(), key=lambda x: x[1]):
    path = reconstruct_path(predecessors, gene)
    print(f"  {gene}: {dist:.2f} via {' -> '.join(path)}")
```

**Most reliable path** (maximize product of confidences instead of minimizing distance): use the identity `max(∏ conf) = min(∑ -log(conf))` to reduce it back to plain Dijkstra.

```python
def most_reliable_path(graph, start, end, confidences):
    """Find the path maximizing the product of edge confidences.

    Hint: max(prod(conf)) == max(sum(log(conf))) == min(sum(-log(conf))),
    so we build a log-transformed graph and run ordinary Dijkstra on it.
    """
    log_graph = WeightedGraph()
    for u, neighbors in graph.adj.items():
        for v, _ in neighbors:
            conf = confidences.get((u, v), confidences.get((v, u), 0.5))
            log_graph.add_edge(u, v, -math.log(conf), directed=True)

    distances, preds = dijkstra(log_graph, start)
    path = reconstruct_path(preds, end)
    reliability = math.exp(-distances[end])
    return path, reliability


conf_scores = {
    ('TP53', 'MDM2'): 0.99, ('TP53', 'BRCA1'): 0.85, ('TP53', 'ATM'): 0.92,
    ('MDM2', 'RB1'): 0.80, ('BRCA1', 'CHEK2'): 0.88, ('ATM', 'CHEK2'): 0.95,
    ('RB1', 'E2F1'): 0.90, ('CHEK2', 'CDC25A'): 0.82,
}
path, rel = most_reliable_path(ppi, 'TP53', 'CDC25A', conf_scores)
print(f"Most reliable path to CDC25A: {' -> '.join(path)}")
print(f"Path reliability: {rel:.4f}")
```

## Network Diameter

**Goal:** Find the diameter of a weighted graph — the longest shortest path between any pair of vertices. In a PPI network this is the maximum signaling distance between any two proteins.

**Approach:** Run Dijkstra from every vertex and keep the largest finite distance seen; O(V) Dijkstra runs, O(V·(V+E) log V) total.

```python
def graph_diameter(graph):
    """Find the diameter of a weighted graph.

    Returns (diameter, source, target, path) for the furthest-apart
    reachable vertex pair.
    """
    best = (0.0, None, None, [])
    for src in graph.vertices():
        distances, preds = dijkstra(graph, src)
        for v, d in distances.items():
            if d != float('inf') and d > best[0]:
                best = (d, src, v, reconstruct_path(preds, v))
    return best


diameter, src, tgt, path = graph_diameter(ppi)
print(f"PPI network diameter: {diameter:.2f}")
print(f"Furthest pair: {src} -> {tgt}")
print(f"Path: {' -> '.join(path)}")
```

## Pitfalls

- **Negative weights break the greedy invariant.** A negative edge can shorten an already-finalized vertex's distance after it's popped. Use Bellman-Ford (O(VE), also detects negative cycles) instead.
- **Stale heap entries.** The same vertex can be pushed multiple times with different tentative distances; always check `if u in visited: continue` after popping, or you'll relax edges from a non-final distance.
- **Missing vertices in directed graphs.** A vertex that only appears as an edge target (no outgoing edges) may not be in `graph.vertices()`; use `distances.get(v, float('inf'))` rather than direct indexing to avoid `KeyError`.
- **Confidence-to-distance conversion.** When converting a similarity/confidence score to an edge weight, use a monotonically decreasing transform (`1 - conf` or `-log(conf)`); do not feed raw confidence scores into Dijkstra as if they were distances — it will find the least, not most, confident path.
- **Undirected edges added twice.** `add_edge(u, v, w)` with `directed=False` inserts the edge in both adjacency lists; passing `directed=True` when you meant undirected silently makes the graph one-way.

## See Also

- `algo-graph-representations` — adjacency list/matrix construction used by `WeightedGraph`.
- `algo-bfs-dfs` — unweighted traversal; use when all edges have equal cost.
- `algo-mst-kruskal-prim` — minimum spanning tree, a related but distinct weighted-graph problem.
- `algo-topological-sort` — required first step for shortest-path algorithms on DAGs with negative weights.
