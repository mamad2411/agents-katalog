---
name: algo-graph-representations
description: Build graph structures (adjacency matrix/list, edge list) in Python/NumPy for PPI, GRN, and metabolic networks. Use when representing a graph, picking sparse vs dense storage, loading an edge-list file, or prepping for BFS/DFS/Dijkstra/MST.
tool_type: python
primary_tool: numpy
---

# Graph Representations

## When to Use

- Modeling a protein-protein interaction (PPI) network, gene regulatory network (GRN), or metabolic network as a graph.
- Deciding between adjacency matrix, adjacency list, and edge list before implementing BFS/DFS, Dijkstra, or Kruskal/Prim MST.
- Loading a graph from a `node_a node_b weight` edge-list file (e.g. STRING/BioGRID exports).
- Estimating memory footprint of a large sparse network (thousands of nodes, sparse edges) before choosing a matrix representation.
- Building a de Bruijn graph (k-mers as vertices, overlaps as edges) for sequence assembly.

## Version Compatibility

Python ≥3.9 (uses `dict`/`list` generic type hints), NumPy ≥1.24. No other dependencies — `collections.defaultdict` is stdlib.

## Prerequisites

- `pip install numpy`
- Familiarity with Big-O notation and basic graph terminology (vertex, edge, degree, directed/undirected).
- Useful follow-on skills: `algo-bfs-dfs`, `algo-dijkstra`, `algo-mst-kruskal-prim`, `networkx`.

## Choosing a Representation

| Operation | Adjacency Matrix | Adjacency List | Edge List |
|-----------|-----------------|----------------|------------|
| Space | O(V²) | O(V + E) | O(E) |
| Add edge | O(1) | O(1) | O(1) |
| Remove edge | O(1) | O(degree) | O(E) |
| Check edge exists | O(1) | O(1) w/ set, O(degree) w/ list | O(E) |
| Get neighbors | O(V) | O(1) access + O(degree) iterate | O(E) |
| Iterate all edges | O(V²) | O(E) | O(E) |

| Scenario | Use |
|----------|-----|
| Dense graph (E ≈ V²) | Adjacency Matrix |
| Sparse graph (most bio networks) | Adjacency List |
| Frequent edge-existence queries on a small graph | Adjacency Matrix |
| BFS / DFS traversal | Adjacency List |
| MST (Kruskal's), streaming from file | Edge List |

**Most biological networks (PPI, GRN, metabolic) are sparse — adjacency lists are almost always the right default.**

| Application | Vertices | Edges |
|------------|----------|-------|
| PPI network | Proteins | Physical interactions |
| Metabolic network | Metabolites | Reactions |
| Gene regulatory network | Genes / TFs | Regulatory relationships |
| de Bruijn graph | k-mers | Sequence overlaps |
| Phylogenetic tree | Species / sequences | Evolutionary relationships |

## Adjacency Matrix

**Goal:** O(1) edge-existence checks for a small, dense graph (e.g. a handful of interacting proteins where you query edges constantly).
**Approach:** Store an N×N NumPy int array indexed by a vertex→index map; set `matrix[i][j] = 1` for each edge, mirroring across the diagonal for undirected graphs.

```python
import numpy as np


class AdjacencyMatrix:
    """Graph representation backed by a dense NumPy adjacency matrix."""

    def __init__(self, vertices: list):
        self.vertices = vertices
        self.idx = {v: i for i, v in enumerate(vertices)}
        self.n = len(vertices)
        self.matrix = np.zeros((self.n, self.n), dtype=int)

    def add_edge(self, u, v, directed: bool = False):
        i, j = self.idx[u], self.idx[v]
        self.matrix[i][j] = 1
        if not directed:
            self.matrix[j][i] = 1

    def has_edge(self, u, v) -> bool:  # O(1)
        return bool(self.matrix[self.idx[u]][self.idx[v]])

    def neighbors(self, u) -> list:  # O(V)
        i = self.idx[u]
        return [self.vertices[j] for j in range(self.n) if self.matrix[i][j]]

    def degree(self, u) -> int:
        return int(np.sum(self.matrix[self.idx[u]]))


# Example: a small p53 signaling PPI network
proteins = ["TP53", "MDM2", "BRCA1", "ATM", "CHEK2"]
interactions = [
    ("TP53", "MDM2"),   # p53-MDM2 negative feedback
    ("TP53", "BRCA1"),  # p53-BRCA1 interaction
    ("ATM", "TP53"),    # ATM phosphorylates p53
    ("ATM", "CHEK2"),   # ATM activates CHEK2
    ("CHEK2", "TP53"),  # CHEK2 phosphorylates p53
    ("BRCA1", "ATM"),   # BRCA1-ATM complex
]
ppi = AdjacencyMatrix(proteins)
for p1, p2 in interactions:
    ppi.add_edge(p1, p2)

assert ppi.has_edge("TP53", "MDM2") is True
assert ppi.degree("TP53") == 4  # MDM2, BRCA1, ATM, CHEK2 all touch TP53
```

## Adjacency List

**Goal:** Efficient storage and traversal for sparse networks (the common case for PPI/GRN graphs with thousands of nodes).
**Approach:** Map each vertex to a `set` of neighbors via `defaultdict(set)` — sets give O(1) edge checks without the O(V²) memory cost of a matrix.

```python
from collections import defaultdict


class AdjacencyList:
    """Sparse graph representation: vertex -> set of neighbors."""

    def __init__(self):
        self.graph: dict = defaultdict(set)  # sets give O(1) edge lookup

    def add_edge(self, u, v, directed: bool = False):
        self.graph[u].add(v)
        if not directed:
            self.graph[v].add(u)

    def has_edge(self, u, v) -> bool:  # O(1) with sets
        return v in self.graph.get(u, set())

    def neighbors(self, u) -> set:  # O(1) access
        return self.graph.get(u, set())

    def degree(self, u) -> int:
        return len(self.graph.get(u, []))

    def edges(self) -> list:  # undirected: each edge reported once
        seen = set()
        result = []
        for u in self.graph:
            for v in self.graph[u]:
                key = tuple(sorted([str(u), str(v)]))
                if key not in seen:
                    seen.add(key)
                    result.append((u, v))
        return result
```

## Edge List and File Loading

**Goal:** Represent (and sort) weighted edges — the natural format for MST algorithms and for parsing tab/space-delimited interaction files (e.g. STRING confidence scores).
**Approach:** Keep a flat list of `(u, v, weight)` tuples; convert to an adjacency list on load for traversal.

```python
from pathlib import Path
from collections import defaultdict


class EdgeList:
    """Weighted edge list, useful for Kruskal's MST and bulk file I/O."""

    def __init__(self):
        self.edges: list[tuple] = []
        self._vertices: set = set()

    def add_edge(self, u, v, weight: float = 1.0):
        self.edges.append((u, v, weight))
        self._vertices.update([u, v])

    def sorted_by_weight(self) -> list:  # for Kruskal's MST
        return sorted(self.edges, key=lambda e: e[2])


def load_edge_list(filepath: str) -> dict[str, list[tuple[str, float]]]:
    """Parse a weighted edge-list file ('node_a node_b weight' per line)
    into an undirected adjacency list: {node: [(neighbor, weight), ...]}.
    """
    graph: dict = defaultdict(list)
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            u, v, w = line.split()
            graph[u].append((v, float(w)))
            graph[v].append((u, float(w)))  # undirected
    return dict(graph)
```

## Memory Analysis (Human PPI: 20,000 proteins, 300,000 interactions)

```python
V, E = 20_000, 300_000
matrix_mb = V * V * 8 / 1e6       # ~3,200 MB
list_mb = (2 * E * 8 + V * 56) / 1e6  # ~5.9 MB
# Ratio: ~542x — adjacency list wins for sparse biological networks
```

## Pitfalls

- **Adjacency matrix for large sparse graphs**: 20k proteins → 3.2 GB matrix for a network that fits in ~6 MB as an adjacency list.
- **List vs set for adjacency list**: using a `list` makes `has_edge` O(degree); use `set` for O(1) lookup if duplicate edges are not needed.
- **Undirected graphs and `edges()`**: naively iterating gives each edge twice; track seen pairs with a set or only emit `u < v`.
- **Vertex not in graph**: indexing a `defaultdict` (`graph[v]`) silently creates an empty entry; use `graph.get(v, set())` for read-only lookups to avoid spurious vertices.
- **Edge list for BFS/DFS**: finding neighbors requires scanning all edges — O(E) per node. Convert to an adjacency list first.

## See Also

- `algo-bfs-dfs` — traversal algorithms built on top of the adjacency list.
- `algo-dijkstra` — shortest paths on weighted graphs represented as adjacency lists.
- `algo-mst-kruskal-prim` — MST algorithms that consume the edge list directly.
- `networkx` — full-featured graph library when you need built-in algorithms instead of hand-rolled representations.
