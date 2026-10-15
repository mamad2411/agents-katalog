---
name: graphology
description: >
  Build, query, and analyze graph data structures using Graphology — the robust,
  multipurpose JavaScript/TypeScript Graph library. Use this skill whenever the
  user is working with graphs, networks, nodes, or edges in JavaScript or
  TypeScript, including: building social networks, dependency graphs, knowledge
  graphs, routing networks, or tree structures; running graph algorithms like
  BFS, DFS, shortest path (Dijkstra, A*), or PageRank; computing centrality
  metrics; detecting communities; applying layouts (ForceAtlas2, force, circular,
  random); importing/exporting GEXF or GraphML files; rendering with sigma.js;
  or asking how to traverse, filter, or analyse any networked data. Also
  triggers on "graphology", "graph object", "graph traversal", "node edges JS",
  "network analysis JavaScript", "sigma.js data", or any request involving
  directed/undirected/mixed graphs in the browser or Node.js.
---

# Graphology

Graphology is a specification and reference implementation for a `Graph` object that supports directed, undirected, and mixed graphs; simple or multi-graphs; self-loops; and attaches arbitrary attributes to nodes, edges, and the graph itself. It emits events, works in both browser and Node.js, and is the data backend for [sigma.js](https://www.sigmajs.org/).

## Installation

```bash
npm install graphology
# Standard library (install only what you need, or install everything):
npm install graphology-metrics graphology-traversal graphology-shortest-path
npm install graphology-layout-forceatlas2 graphology-communities-louvain
# …or install the full bundle:
npm install graphology-library
```

TypeScript types ship with the package (`graphology-types` peer dependency is auto-installed by npm 7+).

---

## Instantiation

```ts
import Graph, {
  DirectedGraph,
  UndirectedGraph,
  MultiGraph,
  MultiDirectedGraph,
  MultiUndirectedGraph,
} from 'graphology';

// Default: simple mixed graph
const g = new Graph();

// Pick the right constructor for your use-case:
const dag   = new DirectedGraph();         // directed, no parallel edges
const road  = new UndirectedGraph();       // undirected, no parallel edges
const multi = new MultiDirectedGraph();    // directed, allows parallel edges

// Options
const g2 = new Graph({ multi: true, allowSelfLoops: false, type: 'directed' });

// Load from serialized data or another Graph instance
const g3 = Graph.from(serializedData);
const g4 = UndirectedGraph.from(existingGraph);
```

**Options:**
| Option | Default | Description |
|---|---|---|
| `type` | `"mixed"` | `"directed"`, `"undirected"`, or `"mixed"` |
| `multi` | `false` | Allow parallel edges between the same pair of nodes |
| `allowSelfLoops` | `true` | Allow edges from a node to itself |

**TypeScript generics** restrict attribute shapes:
```ts
type N = { label: string; color: string };
type E = { weight: number };
type G = { name?: string };

const graph = new Graph<N, E, G>();
```

---

## Building Graphs

### Adding Nodes

```ts
// addNode — throws if key already exists
graph.addNode('alice', { age: 30, city: 'NY' });

// mergeNode — add-or-update (idempotent, safe to call many times)
const [key, wasCreated] = graph.mergeNode('alice', { age: 31 });

// updateNode — always mutates via a function
graph.updateNode('alice', attr => ({ ...attr, age: attr.age + 1 }));
```

Prefer `mergeNode` when building graphs from data streams or when you're not sure the node exists yet.

### Adding Edges

```ts
// addEdge — creates a new edge (auto-generated key)
const edgeKey = graph.addEdge('alice', 'bob', { weight: 5 });

// addEdgeWithKey — you control the key (useful for serialization)
graph.addEdgeWithKey('knows-1', 'alice', 'bob', { since: 2020 });

// mergeEdge — add-or-update (won't create duplicate in a simple graph)
const [key, created] = graph.mergeEdge('alice', 'carol', { weight: 2 });

// Directed vs undirected edges in a mixed graph
graph.addDirectedEdge('alice', 'bob');
graph.addUndirectedEdge('bob', 'carol');
```

### Removing Nodes and Edges

```ts
graph.dropNode('alice');   // also removes all its edges
graph.dropEdge(edgeKey);
graph.clear();             // removes everything
graph.clearEdges();        // removes only edges
```

---

## Reading the Graph

```ts
// Properties
graph.order;              // number of nodes
graph.size;               // number of edges
graph.type;               // "directed" | "undirected" | "mixed"

// Existence checks
graph.hasNode('alice');
graph.hasEdge(edgeKey);
graph.hasEdge('alice', 'bob');  // checks any edge between them

// Edge inspection
graph.source(edgeKey);
graph.target(edgeKey);
graph.extremities(edgeKey);     // [source, target]
graph.isDirected(edgeKey);
graph.isSelfLoop(edgeKey);

// Degree
graph.degree('alice');          // in + out + undirected
graph.inDegree('alice');
graph.outDegree('alice');
graph.undirectedDegree('alice');

// Neighbor check
graph.areNeighbors('alice', 'bob');
```

---

## Attributes

Attributes are plain objects attached to each node, edge, or the graph itself.

```ts
// Node attributes
graph.addNode('alice', { age: 30 });
graph.getNodeAttribute('alice', 'age');        // 30
graph.setNodeAttribute('alice', 'age', 31);
graph.updateNodeAttribute('alice', 'score', n => (n ?? 0) + 1);
graph.mergeNodeAttributes('alice', { city: 'Berlin' });
graph.getNodeAttributes('alice');              // { age: 31, city: 'Berlin' }

// Edge attributes — use the edge key OR source+target shorthand
graph.getEdgeAttribute(edgeKey, 'weight');
graph.getEdgeAttribute('alice', 'bob', 'weight');
graph.setEdgeAttribute(edgeKey, 'weight', 10);

// Batch attribute update (most performant for bulk writes)
graph.updateEachNodeAttributes((node, attr) => ({
  ...attr,
  score: (attr.score ?? 0) + 1,
}), { attributes: ['score'] });  // the hints argument tells listeners what changed

// Graph-level attributes
graph.setAttribute('name', 'My Graph');
graph.getAttribute('name');
```

---

## Iteration

Every iterating method comes in four forms: array (`nodes()`), `forEachNode()`, `mapNodes()`, `filterNodes()`. Same pattern for edges and neighbors.

```ts
// Nodes
const nodes = graph.nodes();               // string[] of all node keys
graph.forEachNode((node, attrs) => { ... });
const labels = graph.mapNodes((node, attrs) => attrs.label);
const adults = graph.filterNodes((node, attrs) => attrs.age >= 18);

// Edges
const edges = graph.edges();              // all edges
graph.edges('alice');                      // edges incident to alice
graph.outEdges('alice');                   // outgoing from alice
graph.inEdges('alice');                    // incoming to alice
graph.forEachEdge((edge, attrs, source, target, sourceAttrs, targetAttrs) => {
  // note: all 6 parameters are available
});

// Neighbors
const friends = graph.neighbors('alice'); // all adjacent nodes
graph.forEachNeighbor('alice', (neighbor, attrs) => { ... });
graph.outNeighbors('alice');              // nodes alice points to
graph.inNeighbors('alice');               // nodes pointing to alice
```

Returning `true` from a `forEachX` callback stops the iteration early (like `Array.prototype.find`).

---

## Serialization

Graphology uses a JSON-friendly format:

```ts
// Export
const data = graph.export();
// {
//   attributes: { name: 'My Graph' },
//   nodes: [{ key: 'alice', attributes: { age: 30 } }],
//   edges: [{ key: 'e1', source: 'alice', target: 'bob',
//             attributes: { weight: 5 }, undirected: false }]
// }

// Import (merges into the graph, does not clear first)
graph.import(data);

// Round-trip via JSON
const json = JSON.stringify(graph.export());
const copy = Graph.from(JSON.parse(json));

// Or use copy helpers
const clone = graph.copy();         // full clone
const empty = graph.emptyCopy();    // same options, no nodes/edges
```

---

## Events

The `Graph` object extends `EventEmitter`:

```ts
graph.on('nodeAdded', ({ key, attributes }) => console.log('added', key));
graph.on('edgeAdded', ({ key, source, target, attributes }) => { ... });
graph.on('nodeDropped', ({ key }) => { ... });
graph.on('attributesUpdated', ({ type, attributes }) => { ... });
graph.on('nodeAttributesUpdated', ({ key, type, attributes }) => { ... });
// also: edgeDropped, cleared, edgesCleared, edgeAttributesUpdated,
//       eachNodeAttributesUpdated, eachEdgeAttributesUpdated
```

---

## Standard Library

Install specific packages or use `graphology-library` for all.

### Traversal (`graphology-traversal`)

BFS and DFS walk the connected component(s) of the graph. Returning `true` from the callback prunes that branch.

```ts
import { bfs, bfsFromNode, dfs, dfsFromNode } from 'graphology-traversal';

// BFS over the entire graph (visits all components)
bfs(graph, (node, attrs, depth) => {
  if (depth >= 3) return true; // prune this branch
  console.log(node);
});

// BFS from a specific starting node
bfsFromNode(graph, 'alice', (node, attrs, depth) => {
  console.log(node, depth);
});

// DFS variants follow the same API
dfsFromNode(graph, 'alice', (node, attrs, depth) => { ... });

// Control traversal direction: 'outbound' (default), 'inbound', 'undirected'
bfsFromNode(graph, 'alice', callback, { mode: 'inbound' });
```

### Shortest Path (`graphology-shortest-path`)

```ts
import { bidirectional, singleSource, dijkstra, astar }
  from 'graphology-shortest-path';

// Unweighted BFS path
const path = bidirectional(graph, 'alice', 'dave'); // ['alice','bob','dave'] | null

// All shortest paths from one source
const paths = singleSource(graph, 'alice'); // { bob: ['alice','bob'], ... }

// Dijkstra (weighted)
const wpath = dijkstra.bidirectional(graph, 'alice', 'dave', 'weight');
const wpaths = dijkstra.singleSource(graph, 'alice', 'weight');

// A* (weighted + heuristic)
const apath = astar.bidirectional(
  graph, 'alice', 'dave',
  (_, attr) => attr.distance,
  (node, target) => euclideanDist(positions[node], positions[target])
);
```

### Metrics (`graphology-metrics`)

All mutating metrics expose an `.assign(graph)` variant that writes results directly onto node/edge attributes — very convenient for rendering.

```ts
import { density } from 'graphology-metrics/graph/density';
import pagerank from 'graphology-metrics/centrality/pagerank';
import betweennessCentrality from 'graphology-metrics/centrality/betweenness';
import degreeCentrality from 'graphology-metrics/centrality/degree';
import closenessCentrality from 'graphology-metrics/centrality/closeness';

// Graph-level
const d = density(graph);

// Centrality — returns { nodeKey: score } map
const pr = pagerank(graph, { alpha: 0.85 });

// Or write scores onto node attributes directly:
pagerank.assign(graph);                         // adds 'pagerank' attribute
betweennessCentrality.assign(graph);            // adds 'betweennessCentrality'
degreeCentrality.assign(graph, { nodeCentralityAttribute: 'dc' });

// Weighted variants
betweennessCentrality.assign(graph, { getEdgeWeight: 'weight' });
betweennessCentrality.assign(graph, { getEdgeWeight: null });  // unweighted
```

### Community Detection (`graphology-communities-louvain`)

```ts
import louvain from 'graphology-communities-louvain';

// Returns { nodeKey: communityId } map
const communities = louvain(graph);

// Write community back onto nodes as 'community' attribute
louvain.assign(graph);
```

### Layouts (`graphology-layout`, `graphology-layout-forceatlas2`)

Layouts compute `x` and `y` attributes for every node.

```ts
import random from 'graphology-layout/random';
import circular from 'graphology-layout/circular';
import forceAtlas2 from 'graphology-layout-forceatlas2';

// Quick initial placement
random.assign(graph);
circular.assign(graph);

// ForceAtlas2 — best for large graphs; run in a WebWorker for the browser

// Option A: .assign() — mutates graph in-place (convenient)
forceAtlas2.assign(graph, {
  iterations: 50,
  settings: forceAtlas2.inferSettings(graph), // derive good defaults from graph size
});

// Option B: raw call — returns a positions map WITHOUT mutating; apply manually
const positions = forceAtlas2(graph, {
  iterations: 50,
  settings: forceAtlas2.inferSettings(graph),
});
// positions = { 'alice': { x: 1.2, y: -0.4 }, 'bob': { ... }, ... }
graph.updateEachNodeAttributes((node, attr) => ({
  ...attr,
  x: positions[node].x,
  y: positions[node].y,
}));
```

### Connected Components (`graphology-components`)

```ts
import { connectedComponents, stronglyConnectedComponents }
  from 'graphology-components';

const components = connectedComponents(graph);  // [[node,...], ...]
const strong = stronglyConnectedComponents(graph);
```

### Operators (`graphology-operators`)

```ts
import { subgraph, reverse, union, intersection }
  from 'graphology-operators';

const sub = subgraph(graph, ['alice', 'bob', 'carol']);
const rev = reverse(graph);  // flip all directed edges
const merged = union(g1, g2);
```

### File Formats (`graphology-gexf`, `graphology-graphml`)

```ts
import { parse, write } from 'graphology-gexf';
// Browser: import { parse, write } from 'graphology-gexf/browser';

const graph = parse(Graph, gexfString);
const gexfOut = write(graph);
```

---

## TypeScript Cheat Sheet

```ts
import Graph, { Attributes } from 'graphology';

// Typed graph
type NodeAttr = { label: string; x: number; y: number; size: number };
type EdgeAttr = { weight: number };
const g = new Graph<NodeAttr, EdgeAttr>();

// Correctly typed iteration
g.forEachNode((node: string, attr: NodeAttr) => { ... });
g.forEachEdge((edge, attr: EdgeAttr, src, tgt) => { ... });
```

---

## Common Patterns and Pitfalls

**Always use named imports for graph subclasses** — the default export is the base `Graph` class. Importing any subclass as the default silently creates a plain `Graph` and breaks multi-edge support:
```ts
// ❌ Default import — 'MultiDirectedGraph' resolves to the base Graph class!
//    multi is false by default; adding parallel edges will throw.
import MultiDirectedGraph from 'graphology';

// ✅ Named imports — every subclass must be destructured
import Graph, {
  DirectedGraph,
  UndirectedGraph,
  MultiGraph,
  MultiDirectedGraph,
  MultiUndirectedGraph,
} from 'graphology';
```

**Use `mergeNode`/`mergeEdge` when streaming data** — they're idempotent and won't throw if the key already exists.

**`addNode` vs `mergeNode`:**
```ts
// ❌ Throws if 'alice' already exists
graph.addNode('alice', { age: 30 });

// ✅ Safe to call multiple times; merges attributes if node exists
graph.mergeNode('alice', { age: 30 });
```

**Retrieving the edge key from source+target in a simple graph:**
```ts
const edgeKey = graph.edge('alice', 'bob'); // null if no edge
```

**Iterating edges of a specific node:**
```ts
// All edges attached to the node
graph.forEachEdge('alice', (edge, attr, source, target) => { ... });
// Only outgoing
graph.forEachOutEdge('alice', (edge, attr, source, target) => { ... });
```

**`updateNodeAttribute` is safer than get+set for concurrent/reactive code:**
```ts
// ✅ Atomic increment — avoids stale-read issues
graph.updateNodeAttribute('alice', 'score', n => (n ?? 0) + 1);
```

**Batch attribute writes are faster than per-node loops:**
```ts
// ✅ Single pass, cache-friendly
graph.updateEachNodeAttributes((node, attr) => ({
  ...attr,
  normalizedScore: attr.score / maxScore,
}));
```

**The `.assign()` convention** — many standard library functions expose a `.assign` variant that writes computed values directly onto graph attributes rather than returning a map. This is the idiomatic pattern for rendering pipelines:
```ts
// Computes and writes 'pagerank', 'betweennessCentrality', 'community'
// onto every node's attributes — then sigma.js (or your renderer) just reads them
pagerank.assign(graph);
betweennessCentrality.assign(graph);
louvain.assign(graph);
```

**Events fire synchronously** — listeners attached via `graph.on()` are called immediately during mutation. Keep them lightweight to avoid performance issues.

**Sigma.js integration** — graphology is the data layer for sigma.js. Build and populate the graph (with `x`, `y`, `size`, `label`, `color` node attributes), then hand it to sigma:
```ts
import Sigma from 'sigma';
const renderer = new Sigma(graph, container);
```

---

## Related Skills

| Skill | How it complements Graphology |
|---|---|
| **rete-js** | Rete.js builds interactive visual node editors with drag-and-drop wiring. Graphology can serve as the underlying data model for the graph Rete.js displays — especially useful when you need to run algorithms (shortest path, centrality) on the same graph the visual editor exposes. |
| **physics** | ForceAtlas2 and force-directed layouts are particle simulations under the hood (repulsion + attraction forces, Euler/Verlet integration). Understanding spring-mass physics and numerical integration helps you tune FA2 settings (`gravity`, `scalingRatio`, `barnesHutOptimize`) and build custom force layouts. |
| **geometry** | When building interactive graph visualisers you often need spatial queries: pick the node closest to the mouse cursor, detect hover over an edge, or perform ray-vs-bounding-box tests on node sprites. The geometry skill covers these spatial tests. |
| **animation-specialist** | Animating graph transitions — nodes fading in, edges morphing, layout interpolation between two states — requires lerping x/y positions frame-by-frame via `requestAnimationFrame` or a GSAP ticker. The animation skill covers easing, spring dynamics, and the keyframe patterns needed. |
| **web-visual-effects** | Sigma.js renders to WebGL. When you need custom node shaders, edge glow effects, post-processing passes, or particle overlays on top of a graph scene, the web-visual-effects skill covers WebGL/WebGPU programming and PixiJS patterns that integrate with a sigma.js canvas. |

---

## Reference

- Full API docs: https://graphology.github.io/
- Standard library index: https://graphology.github.io/standard-library/
- GitHub: https://github.com/graphology/graphology
- Sigma.js (rendering): https://www.sigmajs.org/
