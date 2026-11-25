---

name: lease-epoch-fencing-token-monotonic-guard
description: Reject stale leader writes using a monotonic epoch/fencing token rather than just liveness checks
category: algorithms
triggers:
  - lease epoch fencing token monotonic guard
tags: [algorithms, lease, epoch, fencing, token, monotonic]
version: 1.0.0
---

# lease-epoch-fencing-token-monotonic-guard

When building leader-election visualizations, the naive "only the leader can write" rule breaks under partition-heal scenarios: an old leader that didn't notice it lost the lease still thinks it's leader and keeps issuing writes. The fix is a fencing token — a monotonically increasing integer assigned on each leader election. Every write carries the token; the state machine rejects any write whose token is less than the highest seen.

```js
class StateMachine {
  apply(op, token) {
    if (token < this.maxToken) return { rejected: 'stale-leader' };
    this.maxToken = token;
    this.state = reduce(this.state, op);
  }
}
```

This pattern generalizes far beyond leader election: any resource with exclusive access under partial failure benefits (distributed locks, cache invalidation epochs, config version pins, optimistic concurrency versions). The key insight is that liveness checks alone ("is the leader still alive?") race against the network — a write that *was* authorized when sent may arrive after authority transferred. Attaching a monotonic token moves the check to the receiver at apply time, eliminating the race entirely. For visualizations, showing the rejected write with its stale token next to the current token makes the failure mode legible in a way that abstract "split-brain" diagrams don't.
