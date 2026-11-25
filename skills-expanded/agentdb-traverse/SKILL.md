---
name: agentdb-traverse
description: K-hop traversal from a starting node in AgentDB's graph. Use to explore neighborhoods, find reachable nodes, or visualize a memory's "context".
---

# K-Hop Traverse

Walk outward from a node up to K hops, returning the visited subgraph.

## When to use

- "Show me what's connected to X"
- Building a context window from a starting fact + everything causally linked to it
- Visualizing a memory's neighborhood for the user
- Pre-fetch for an investigator agent before running causal_explain

## API

```
agentdb_kHopNeighbors(
  startId:        <node id>
  k:              1..5                 // hops
  edgeFilter?:    [<relation>, ...]    // limit to specific relations
  direction?:     'in' | 'out' | 'both'
  maxNodes?:      100                  // safety cap
)

Returns: { nodes, edges, stats: { reachable, capped } }
```

## Patterns

| Goal | Pattern |
|---|---|
| Forward influence | `direction: 'out'`, `k: 3` |
| Backward dependencies | `direction: 'in'`, `k: 3` |
| Local neighborhood | `direction: 'both'`, `k: 1` |
| Causal chain only | `edgeFilter: ['caused', 'supersedes']` |
| Skill composition graph | `edgeFilter: ['composes', 'requires']`, start: skill id |

## Output sizing

K-hop fans out exponentially. With average degree d, k hops returns up to `d^k` nodes. AgentDB defaults `maxNodes: 100` — when you hit the cap, `stats.capped: true` and you should rerun with smaller k or tighter edgeFilter.

## Don't

- Don't traverse with `k > 4` without `edgeFilter` — explosive fan-out destroys the answer's signal.
- Don't render the whole subgraph to the user. Pick the top-15 by uplift and summarize the rest.
