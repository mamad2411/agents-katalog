---

name: concurrent-edit-merge-arbitration-table
description: Resolve concurrent replica writes via a deterministic tie-breaker table keyed on causal-compare results plus a stable replica priority.
category: algorithms
triggers:
  - concurrent edit merge arbitration table
tags: [algorithms, concurrent, edit, merge, arbitration, table]
version: 1.0.0
---

# concurrent-edit-merge-arbitration-table

When two replicas produce versions whose causal metadata compares as "concurrent" (neither happens-before the other), naive last-write-wins loses data and causes divergence across replicas that see the writes in different orders. The reusable pattern is a small arbitration table that maps `(compareResult, localReplicaId, remoteReplicaId)` to a deterministic winner — so every replica, regardless of arrival order, picks the same survivor.

Structure the table in three tiers: (1) if `compare(a,b) === BEFORE` pick b, if `AFTER` pick a, if `EQUAL` no-op; (2) if `CONCURRENT`, fall through to a stable per-field merge policy (set-union, max, LWW-with-replica-id); (3) if the policy can't merge (e.g. scalar with no semilattice), break ties by `(wallClock, replicaId)` lexicographically where `replicaId` is a fixed UUID — never a dynamic rank. The key insight: the replicaId tiebreaker must be the LAST resort, not the first, or you silently drop legitimately-ordered writes.

```ts
function arbitrate(a: Versioned, b: Versioned): Versioned {
  const cmp = causalCompare(a.clock, b.clock);
  if (cmp === 'BEFORE') return b;
  if (cmp === 'AFTER') return a;
  if (cmp === 'EQUAL') return a;
  const merged = tryLatticeMerge(a, b);
  if (merged) return merged;
  return (a.wall, a.replicaId) > (b.wall, b.replicaId) ? a : b;
}
```
Encode the table as data (object literal or switch), not scattered if-chains, so the determinism is auditable and the fallback order is visible at a glance.
