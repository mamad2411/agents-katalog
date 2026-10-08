---
name: sagemath
description: Run SageMath computations for graph theory, combinatorics, algebra, and mathematical verification. Use for chromatic polynomials, automorphism groups, Tutte polynomials, spectral analysis, and any computation beyond NetworkX/SymPy.
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"requires":{"bins":["bash"]}}}
---

# SageMath

Use this skill for mathematical computations that need SageMath — especially graph theory (chromatic polynomial, automorphism groups, Tutte polynomial), combinatorics, polynomial algebra, finite fields, and spectral analysis.

For simple graph checks (connectivity, bipartiteness), use NetworkX directly in the sandbox instead — it's faster (no container overhead).

## Usage

Write Sage code and execute via:
```
exec: /workspace/skills/sagemath/run_sage.sh "<sage_code>"
exec: /workspace/skills/sagemath/run_sage.sh --timeout 1800 "<sage_code>"
exec: /workspace/skills/sagemath/run_sage.sh --file /workspace/script.sage
exec: /workspace/skills/sagemath/run_sage.sh --save "label" "<sage_code>"
exec: /workspace/skills/sagemath/run_sage.sh --plot "<sage_code_that_returns_plot>"
exec: /workspace/skills/sagemath/run_sage.sh --session "mysession" "<sage_code>"
exec: /workspace/skills/sagemath/run_sage.sh --cancel <job_id>
```

The code runs inside a Docker container with 3 CPUs, 16GB RAM, no network access.

Output is JSON: `{"status": "ok", "output": "...", "duration_seconds": N}` on success, `{"status": "error", "message": "..."}` on failure.

### Options

- `--timeout N` — seconds before kill (default: 300). Use 1800 for batch jobs.
- `--save "label"` — also saves result to `{{ PRIVATE_DATA_DIR }}/research/sagemath/<label>.json`
- `--plot` — detects saved plot image, returns `"plot": "/path/to/image.png"` in result. Send via `send_file.sh`.
- `--session "name"` — appends code to a persistent session file, re-runs the full session. Use for multi-step computations.
- `--cancel <job_id>` — cancels a running job by ID.
- `--file <path>` — execute a `.sage` script file instead of inline code.

### Templates

Pre-built research scripts in `/workspace/skills/sagemath/templates/`. Run via `--file`:

```
exec: /workspace/skills/sagemath/run_sage.sh --file /workspace/skills/sagemath/templates/enumerate_chromatic.sage
exec: /workspace/skills/sagemath/run_sage.sh --file /workspace/skills/sagemath/templates/counterexample_search.sage
exec: /workspace/skills/sagemath/run_sage.sh --file /workspace/skills/sagemath/templates/spectral_analysis.sage
exec: /workspace/skills/sagemath/run_sage.sh --file /workspace/skills/sagemath/templates/reconfiguration_check.sage
```

Templates accept parameters via environment variables. Set them by prefixing the docker exec:
- `enumerate_chromatic.sage` — `SAGE_PARAM_N=6` (number of vertices)
- `counterexample_search.sage` — `SAGE_PARAM_N_MAX=7`, `SAGE_PARAM_CONJECTURE="G.chromatic_number() <= G.clique_number() + 1"`
- `spectral_analysis.sage` — `SAGE_PARAM_FAMILY=CycleGraph`, `SAGE_PARAM_N_MIN=3`, `SAGE_PARAM_N_MAX=10`
- `reconfiguration_check.sage` — `SAGE_PARAM_N=5`, `SAGE_PARAM_K=3`, `SAGE_PARAM_GRAPH=CycleGraph`

## Sage quick reference

### Creating graphs
```python
G = Graph([(0,1),(1,2),(2,3),(3,0)])       # from edge list
G = Graph({0:[1,2], 1:[2,3], 3:[0]})       # from adjacency dict
G = graphs.PetersenGraph()
G = graphs.CompleteGraph(5)
G = graphs.CycleGraph(6)
G = graphs.PathGraph(4)
G = graphs.KneserGraph(5,2)
G = graphs.CompleteMultipartiteGraph([3,3,3])
G = graphs.Grid2dGraph(4,4)
```

### Chromatic polynomial & coloring
```python
G.chromatic_polynomial()         # x^5 - 5*x^4 + 10*x^3 - 10*x^2 + 4*x (for C5)
G.chromatic_number()             # 3
G.chromatic_index()              # edge chromatic number
G.coloring(algorithm="DLX")      # returns color assignment
G.fractional_chromatic_number()
```

### Automorphism group
```python
G.automorphism_group().order()                  # 120 for Petersen
G.automorphism_group().structure_description()  # "S5"
G.is_isomorphic(H)
```

### Tutte polynomial
```python
G.tutte_polynomial()  # x^3 + y^3 + 3*x^2 + 4*x*y + 3*y^2 + 2*x + 2*y (for K4)
```

### Spectral analysis
```python
G.adjacency_matrix()
G.laplacian_matrix()
G.characteristic_polynomial()  # x^4 - 4*x^2 (for C4)
G.spectral_radius()
```

### Independent sets, dominating sets, structural properties
```python
G.independent_set()
G.vertex_cover()
G.dominating_set()
G.treewidth()
G.clique_number()
G.matching()
G.is_planar()
G.genus()
G.hamiltonian_cycle()
```

### Parallel computation
```python
from sage.parallel.decorate import parallel

@parallel(ncpus=3)
def compute(n):
    return graphs.CompleteGraph(n).chromatic_polynomial()

results = list(compute([5,6,7,8]))
for inp, out in results:
    print(f"K_{inp[0][0]}: {out}")
```

### File I/O
```python
# Save/load graphs
G.export_to_file("{{ PRIVATE_DATA_DIR }}/research/sagemath/graph.g6", format="graph6")
H = Graph("{{ PRIVATE_DATA_DIR }}/research/sagemath/graph.g6", format="graph6")

# Save results as JSON
import json
result = {"chromatic_number": int(G.chromatic_number()), "treewidth": int(G.treewidth())}
with open("{{ PRIVATE_DATA_DIR }}/research/sagemath/result.json", "w") as f:
    json.dump(result, f)
```

### Algebra over finite fields
```python
from sage.all import GF, matrix, PolynomialRing
M = matrix(GF(7), [[1,2],[3,4]])
M.det()        # 5
M.eigenvalues()

R = PolynomialRing(QQ, 'x')
x = R.gen()
f = x^3 - 2*x + 1
f.roots()
```

## Key methods (64 relevant for graph theory)

chromatic_polynomial, chromatic_number, chromatic_index, coloring, fractional_chromatic_number, automorphism_group, tutte_polynomial, adjacency_matrix, laplacian_matrix, characteristic_polynomial, spectral_radius, independent_set, vertex_cover, dominating_set, treewidth, clique_number, clique_maximum, matching, perfect_matchings, is_planar, genus, hamiltonian_cycle, hamiltonian_path, is_isomorphic, edge_connectivity, vertex_connectivity, flow, matching_polynomial, chromatic_symmetric_function, chromatic_quasisymmetric_function, and more.

## Graph generators (280 available)

CompleteGraph, CycleGraph, PathGraph, PetersenGraph, KneserGraph, JohnsonGraph, Grid2dGraph, CompleteMultipartiteGraph, CompleteBipartiteGraph, RandomGNP, BalancedTree, GeneralizedPetersenGraph, and more.
