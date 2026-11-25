---
name: algo-mst-kruskal-prim
description: "Compute minimum spanning trees with Kruskal's (Union-Find) and Prim's (min-heap) algorithms in Python or networkx. Use when building a phylogenetic distance tree, gene co-expression network backbone, MST-based clustering, or implementing Union-Find/disjoint-set."
tool_type: python
primary_tool: networkx
---

# Minimum Spanning Trees (Kruskal & Prim)

An MST connects all V vertices with exactly V-1 edges at minimum total weight. It is unique when all edge weights are distinct.

**Cut property:** for any partition of the vertices into two sets, the minimum-weight edge crossing the partition must be in some MST. This is why the greedy Kruskal/Prim approach is correct, not just heuristic.

## When to Use
- Collapsing a pairwise distance matrix (e.g., species divergence, gene correlation) into a minimum-cost tree
- Building a gene co-expression network "backbone" from a correlation-distance matrix
- Single-linkage hierarchical clustering by cutting the longest MST edges
- Minimum-cost network/wiring design problems (connect all nodes cheaply)
- Implementing or explaining Union-Find (disjoint set) with path compression and union by rank

## Version Compatibility
Pure Python (stdlib `heapq`, `collections`) — Python ≥3.9. Optional production path: networkx ≥3.0 (`nx.minimum_spanning_tree`/`minimum_spanning_edges`, Kruskal by default) or scipy ≥1.10 (`scipy.sparse.csgraph.minimum_spanning_tree` for large sparse graphs).

## Prerequisites
- `pip install networkx scipy` (only needed for the library-based path)
- Graph representation basics — see `algo-graph-representations`
- Comfortable with adjacency lists/matrices and basic graph traversal — see `algo-bfs-dfs`

**Goal:** find the minimum-weight edge set connecting all vertices.
**Approach:** Union-Find backs Kruskal's cycle check in near-O(1) amortized time via path compression + union by rank.

```python
class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """Return the representative (root) of x's set, compressing the path."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        """Merge x's and y's sets. Returns False if already in the same set (cycle)."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

**Goal:** MST from an edge list, e.g. a simplified phylogeny from pairwise distances.
**Approach:** sort edges by weight ascending; greedily accept an edge if its endpoints are in different Union-Find components; stop after V-1 edges.

```python
def kruskal(vertices, edges):
    """Kruskal's MST algorithm.

    vertices: list of vertex labels
    edges: list of (u, v, weight)
    Returns (mst_edges, total_weight). Time: O(E log E).
    """
    vertex_idx = {v: i for i, v in enumerate(vertices)}
    uf = UnionFind(len(vertices))
    mst, total = [], 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(vertex_idx[u], vertex_idx[v]):
            mst.append((u, v, w))
            total += w
            if len(mst) == len(vertices) - 1:
                break
    return mst, total

species = ["Human", "Chimp", "Gorilla", "Orangutan", "Mouse"]  # simplified phylogeny example
distances = [
    ("Human", "Chimp", 1.2), ("Human", "Gorilla", 1.6), ("Human", "Orangutan", 3.1),
    ("Human", "Mouse", 8.5), ("Chimp", "Gorilla", 1.5), ("Chimp", "Orangutan", 3.0),
    ("Chimp", "Mouse", 8.4), ("Gorilla", "Orangutan", 2.8), ("Gorilla", "Mouse", 8.3),
    ("Orangutan", "Mouse", 8.1),
]
mst, total = kruskal(species, distances)
for u, v, w in mst:
    print(f"{u} -- {v}: {w}")
print(f"Total evolutionary distance: {total}")
```

**Goal:** same MST, but grown from a start node — preferred on dense graphs (E close to V^2).
**Approach:** maintain a min-heap of candidate edges leaving the visited set; pop the cheapest edge to an unvisited vertex, repeat.

```python
import heapq
from collections import defaultdict

def prim(vertices, adj):
    """Prim's MST algorithm.

    adj: {vertex: [(neighbor, weight), ...]} (undirected, both directions present)
    Returns (mst_edges, total_weight). Time: O((V + E) log V).
    """
    start = vertices[0]
    visited = {start}
    mst, total = [], 0
    heap = [(w, start, v) for v, w in adj[start]]
    heapq.heapify(heap)
    while heap and len(visited) < len(vertices):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue  # stale entry for an already-connected vertex
        visited.add(v)
        mst.append((u, v, w))
        total += w
        for neighbor, weight in adj[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (weight, v, neighbor))
    return mst, total

adj = defaultdict(list)
for u, v, w in distances:
    adj[u].append((v, w))
    adj[v].append((u, w))
mst_prim, total_prim = prim(species, adj)
```

**Goal:** MST-based single-linkage clustering into k groups.
**Approach:** compute the MST, drop the k-1 heaviest edges, and read off connected components with Union-Find.

```python
def mst_clustering(vertices, edges, k=2):
    """Cut the k-1 longest MST edges to produce k clusters (single-linkage equivalent)."""
    mst, _ = kruskal(vertices, edges)
    mst_sorted = sorted(mst, key=lambda e: e[2], reverse=True)
    kept = mst_sorted[k - 1:]
    uf = UnionFind(len(vertices))
    vertex_idx = {v: i for i, v in enumerate(vertices)}
    for u, v, w in kept:
        uf.union(vertex_idx[u], vertex_idx[v])
    clusters = defaultdict(list)
    for v in vertices:
        clusters[uf.find(vertex_idx[v])].append(v)
    return list(clusters.values())

clusters = mst_clustering(species, distances, k=2)
```

**Goal:** production use on real graphs without hand-rolling Union-Find.
**Approach:** build a weighted networkx graph and call the built-in MST routine (Kruskal by default; pass `algorithm="prim"` for the alternative).

```python
import networkx as nx

def networkx_mst(vertices, edges):
    """Build MST with networkx; returns list of (u, v, weight) edges."""
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    T = nx.minimum_spanning_tree(G, algorithm="kruskal")
    return [(u, v, d["weight"]) for u, v, d in T.edges(data=True)]

mst_edges = networkx_mst(species, distances)
```

## Kruskal vs Prim

| | Kruskal | Prim |
|---|---|---|
| Time | O(E log E) | O((V+E) log V) |
| Best for | Sparse graphs | Dense graphs |
| Data structure | Union-Find | Min-heap |

## Pitfalls
- Kruskal without Union-Find (naive cycle detection via DFS) degrades to O(VE) — always use the disjoint-set check.
- Prim's heap accumulates stale entries for already-visited vertices; the `if v in visited: continue` skip is required, not optional.
- Equal-weight edges can yield different but equally valid MSTs — do not assume a unique output when comparing to a reference tree.
- `mst_clustering` assumes the graph is connected; a disconnected input silently produces a spanning *forest*, not a tree, and cutting k-1 edges won't give exactly k clusters.
- Kruskal needs an edge list; Prim needs an adjacency list — building the wrong structure is the most common integration bug when swapping algorithms.

## See Also
- `algo-graph-representations` — adjacency list/matrix construction feeding both algorithms
- `algo-dijkstra` — contrasts MST (cheapest tree) with shortest-path tree (cheapest paths from one source)
- `algo-bfs-dfs` — traversal primitives used to validate/inspect the resulting tree
- `bio-core-phylogenetics` — pairwise distance matrices that feed Kruskal/Prim for tree building
