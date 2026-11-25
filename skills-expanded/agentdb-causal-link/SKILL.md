---
name: agentdb-causal-link
description: Record a causal relationship between two memories in AgentDB — "X caused Y", "A supersedes B", "patch-foo depends-on patch-bar". Use when the user is documenting cause/effect, dependencies, supersessions, or after-action analysis.
---

# Link Causally

Add a typed edge between two memories so future queries can traverse cause→effect, supersedes, depends-on, etc.

## When to use

- User says "X caused Y", "this depends on that", "this supersedes the old one"
- Post-incident analysis — recording what led to what
- Building a knowledge graph from a sequence of episodes
- ADR housekeeping — `supersedes` / `amends` / `related-to` between architecture decisions

## API

```
agentdb_causal_edge(
  fromMemoryId:   <id>
  fromMemoryType: 'episode' | 'pattern' | 'skill' | 'adr'
  toMemoryId:     <id>
  toMemoryType:   <same set>
  relation:       'caused' | 'supersedes' | 'depends-on' | 'related-to' | <custom>
  similarity?:    0..1
  uplift?:        -1..1   // signed reward delta
  confidence?:    0..1
  metadata?:      { evidenceCount, sourceTimestamp, ... }
)
```

`uplift` is the secret sauce. Positive uplift = the causal link improved outcomes; negative = it hurt. The `agentdb-investigator` agent (this plugin) walks edges weighted by uplift × confidence to find root causes.

## Cascade-aware delete

The agentdb 3.0.0-alpha.13 release added `cascade: true` semantics:

- `agentdb_causal_edge_delete(edgeId)` — single edge
- `agentdb_causal_node_delete(nodeId, { cascade: true })` — node + all incident edges; returns deletedEdges count
- `agentdb_edges_by_endpoints(from, to, label?)` — bulk delete by tuple

Use cascade when removing an obsolete ADR or decommissioning an agent — leaving dangling edges in the graph poisons future traversals.

## Don't

- Don't link memories without confidence < 0.5 unless you mark them as conjectures. Low-confidence edges accumulate and degrade `agentdb_causal_explain` quality.
- Don't use `caused` for correlation — reserve it for genuinely causal evidence (controlled change, repeated observation, expert confirmation).
- Don't forget the inverse direction. "A supersedes B" implies B is no longer authoritative; tag B's hierarchical entry as deprecated in the same operation.
