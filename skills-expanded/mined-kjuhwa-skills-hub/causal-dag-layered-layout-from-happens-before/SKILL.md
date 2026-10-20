---

name: causal-dag-layered-layout-from-happens-before
description: Layout a DAG of events by longest happens-before depth per actor lane for readable causal diagrams.
category: frontend
triggers:
  - causal dag layered layout from happens before
tags: [frontend, causal, dag, layered, layout, happens]
version: 1.0.0
---

# causal-dag-layered-layout-from-happens-before

When visualizing event histories across multiple actors/replicas, naive timestamp-based X positioning produces crossing arrows and visual ambiguity because wall-clock time doesn't match logical causal order. The reusable trick is to assign each event an integer `layer = 1 + max(layer(p) for p in parents)` computed by a topological walk over the happens-before edges, then render the actor as the Y lane and `layer` as the X column. Concurrent events end up in the same column only when they're truly concurrent, and every causal arrow points strictly rightward.

```js
function assignLayers(events, hb) { // hb: id -> parent ids
  const layer = new Map();
  const visit = id => {
    if (layer.has(id)) return layer.get(id);
    const parents = hb[id] ?? [];
    const l = parents.length ? 1 + Math.max(...parents.map(visit)) : 0;
    layer.set(id, l);
    return l;
  };
  events.forEach(e => visit(e.id));
  return layer; // x = layer*COL_W, y = actorIndex*ROW_H
}
```

This generalizes to any causal/provenance UI: git-like commit graphs, build pipelines, trace spans with explicit parent edges, CRDT operation logs. Pair it with a second pass that spreads equal-layer events vertically within an actor lane when the lane has multiple concurrent writes, and arrows never cross their own source column.
