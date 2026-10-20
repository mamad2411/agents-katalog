---

name: consistent-hash-ring-virtual-node-placement
description: Place virtual nodes on a hash ring using salted hashes to smooth load distribution across physical shards.
category: algorithms
triggers:
  - consistent hash ring virtual node placement
tags: [algorithms, consistent, hash, ring, virtual, node]
version: 1.0.0
---

# consistent-hash-ring-virtual-node-placement

When mapping keys to shards via a hash ring, a single hash per physical node causes uneven load — some arcs of the ring cover 3x more key-space than others. The fix is to generate N virtual nodes per physical node by hashing `nodeId + ":" + replicaIndex` for replicaIndex in 0..N-1, then inserting each virtual node into a sorted ring. N=100-200 typically brings variance under 5%.

```js
function buildRing(nodes, vnodesPerNode = 150) {
  const ring = []; // {hash, nodeId}
  for (const node of nodes) {
    for (let i = 0; i < vnodesPerNode; i++) {
      ring.push({ hash: fnv1a(`${node.id}:${i}`), nodeId: node.id });
    }
  }
  return ring.sort((a, b) => a.hash - b.hash);
}
function lookup(ring, key) {
  const h = fnv1a(key);
  // binary search for first vnode with hash >= h, wrap around
  return ring[bisectLeft(ring, h) % ring.length].nodeId;
}
```

Key insight: virtual node count is a tunable knob. Low N (10) shows visible hotspots useful for teaching; high N (500+) flattens the distribution. Expose N as a slider in visualizations so users can see the variance-vs-memory tradeoff directly.
