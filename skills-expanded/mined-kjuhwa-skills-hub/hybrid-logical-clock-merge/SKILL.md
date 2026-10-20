---

name: hybrid-logical-clock-merge
description: Merge wall-clock time with logical counter to get monotonic timestamps that survive clock skew and concurrent events.
category: algorithms
triggers:
  - hybrid logical clock merge
tags: [algorithms, hybrid, logical, clock, merge]
version: 1.0.0
---

# hybrid-logical-clock-merge

When building causality-aware systems, pure Lamport counters lose wall-clock meaning and pure wall-clocks violate causality under skew. A Hybrid Logical Clock (HLC) stores `(physicalMs, logical)` and on every local event does `physical = max(nowMs, lastPhysical)`; if physical equals last, `logical++`, else `logical = 0`. On receive, `physical = max(nowMs, localPhysical, remotePhysical)` with the logical counter bumped only on ties. This yields timestamps that are (a) close to real time for humans, (b) strictly monotonic per node, (c) consistent with causality across nodes.

```js
function tickLocal(hlc, nowMs) {
  const p = Math.max(nowMs, hlc.p);
  return { p, l: p === hlc.p ? hlc.l + 1 : 0 };
}
function tickRecv(hlc, remote, nowMs) {
  const p = Math.max(nowMs, hlc.p, remote.p);
  const l = p === hlc.p && p === remote.p ? Math.max(hlc.l, remote.l) + 1
          : p === hlc.p ? hlc.l + 1
          : p === remote.p ? remote.l + 1 : 0;
  return { p, l };
}
```

Display HLCs as `p.l` so humans can still reason about "roughly when." Use them as sort keys for event logs where you need both approximate wall-time order and a total tiebreaker that respects causality — strictly better than either component alone.
