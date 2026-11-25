---
name: agentdb-hyperedge
description: Search and manage hyperedges — n-ary relationships between memories. Use for swarm membership, multi-cause incidents, or any "this involves all of (A, B, C, D)" relationship that doesn't fit a binary edge.
---

# Hyperedge

Hyperedges connect more than two nodes — useful when a single relationship genuinely involves many participants.

## When to use

- **Swarm membership** — "agents A, B, C, D worked together on task T"
- **Multi-cause incidents** — "outage was caused by (deploy, traffic spike, cache miss, retry storm)"
- **Group decisions** — "ADR-046 was approved by reviewers (alice, bob, carol, dan)"
- Anything where binary edges would lose information by splitting the relationship

## API

```
agentdb_hyperedge_create(
  nodes:        [<id>, <id>, ...]
  description:  <one-liner>
  embedding?:   Float32Array
  confidence?:  0..1
  metadata?:    { ... }
)

agentdb_hyperedge_search(
  query:        <semantic | nodeId>
  topK?:        10
)

agentdb_hyperedge_delete(
  id:           <hyperedge id>
)
```

The `agentdb_hyperedge_delete` tool was added in agentdb 3.0.0-alpha.13.

## Semantic search over hyperedges

Hyperedges are searchable by their description embedding — useful for "find all multi-agent collaborations on auth-related work" without enumerating every binary edge.

## Don't

- Don't use a hyperedge when a binary edge fits. Two-node "caused" links are cheaper to reason about.
- Don't put more than ~10 nodes in one hyperedge. After that, the relationship is too broad to mean anything specific.
