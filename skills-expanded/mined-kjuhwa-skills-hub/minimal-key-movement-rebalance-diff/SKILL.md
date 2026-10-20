---

name: minimal-key-movement-rebalance-diff
description: Compute the set of keys that must move when a shard is added/removed by diffing ring ownership before and after.
category: algorithms
triggers:
  - minimal key movement rebalance diff
tags: [algorithms, minimal, key, movement, rebalance, diff]
version: 1.0.0
---

# minimal-key-movement-rebalance-diff

A common mistake in rebalance visualizations is to re-hash every key and show every key "moving." In a properly-built consistent hash ring, adding one node only moves ~1/N of keys (the arcs the new node now owns). To render this correctly, snapshot ownership before the topology change, apply the change, then emit a diff event only for keys whose owner changed.

```js
function rebalanceDiff(ringBefore, ringAfter, keys) {
  const moves = [];
  for (const key of keys) {
    const from = lookup(ringBefore, key);
    const to = lookup(ringAfter, key);
    if (from !== to) moves.push({ key, from, to });
  }
  return moves; // length should be ~keys.length / nodeCount
}
```

This diff is the honest visualization of rebalance cost. Animate only the moved keys traveling from old to new owner; leave the rest static. Users instantly grasp why consistent hashing matters — because 90%+ of the keys don't move. A naive re-hash would show all keys migrating, which is visually busy and factually wrong.
