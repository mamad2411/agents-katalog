---
name: agentdb-hierarchical-store
description: Store memories in tier-aware hierarchical memory — working / short-term / long-term — and recall with tier filters. Use for working-set context that should fade, vs facts that should persist, vs patterns that should be searchable forever.
---

# Hierarchical Store

Three-tier memory matching how humans actually use memory. Each tier has different retention, retrieval cost, and query semantics.

## Tiers

| Tier | Retention | Use for |
|---|---|---|
| **working** | minutes (auto-expires) | The current task's scratch — files open, hypotheses, in-flight decisions |
| **short** | hours-days | Recent session context — what was decided this morning |
| **long** | indefinite (until pruned) | Cross-session facts, patterns, lessons |

## API

```
agentdb_hierarchical_store(
  key:      <namespace key>           // e.g. 'task:auth-refactor:hypothesis'
  tier:     'working' | 'short' | 'long'
  value:    <stringified content>
  ttl?:     <seconds>                 // overrides tier default
  metadata?: { topic, project, ... }
)

agentdb_hierarchical_recall(
  query:    <semantic or exact key>
  tier?:    <filter>                  // omit to search all tiers
  k?:       5
)

agentdb_hierarchical_delete(
  key:      <namespace key>
  tier?:    <filter>
)
```

The delete tool was added in agentdb 3.0.0-alpha.13. Before that, there was no first-class way to remove an entry — re-indexing workflows like ruflo's `/adr-index` couldn't purge stale ADRs. Now they can.

## Recall flow

1. Query `working` first — it's smallest, freshest, highest signal for "what am I doing right now."
2. Fall back to `short` if working returns nothing.
3. Search `long` last for established knowledge.
4. Or search all three with `tier=undefined` and let the bandit weight by tier × similarity.

## Don't

- Don't put long-term facts in `working` — they expire and you lose them.
- Don't put session scratch in `long` — it pollutes searches forever.
- Don't forget to set TTL when overriding tier defaults; the engine won't infer it.
