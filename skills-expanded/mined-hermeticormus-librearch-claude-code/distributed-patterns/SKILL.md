---
name: "distributed-patterns"
description: "Distributed systems patterns with code: a consistent hashing ring, a simplified Raft leader election state machine, fencing tokens for safe locks, and SWIM gossip failure detection. Use when implementing coordination, partitioning, or failure detection."
---

# Distributed Systems Patterns

> Named patterns with code for consistent hashing, Raft leader election steps, Redlock distributed locking, gossip fanout, partition handling, and fencing tokens.

## Patterns

### Pattern: Consistent Hashing Ring (Python)

Full implementation with virtual nodes, node addition/removal, and distribution analysis:

```python
import hashlib
import bisect
from collections import defaultdict
from typing import Optional

class ConsistentHashRing:
    """
    Consistent hashing with virtual nodes.
    Adding/removing a node moves only 1/n keys (vs n-1/n for modulo hashing).
    """

    def __init__(self, virtual_nodes: int = 150):
        self.virtual_nodes = virtual_nodes
        self.ring: dict[int, str] = {}
        self.sorted_keys: list[int] = []
        self._nodes: set[str] = set()

    def add_node(self, node: str) -> list[str]:
        """Add node. Returns list of keys that moved to this node."""
        self._nodes.add(node)
        for i in range(self.virtual_nodes):
            pos = self._hash(f"{node}:{i}")
            self.ring[pos] = node
            bisect.insort(self.sorted_keys, pos)
        return []  # Key migration tracking omitted for brevity

    def remove_node(self, node: str):
        self._nodes.discard(node)
        for i in range(self.virtual_nodes):
            pos = self._hash(f"{node}:{i}")
            if pos in self.ring:
                del self.ring[pos]
                idx = bisect.bisect_left(self.sorted_keys, pos)
                if idx < len(self.sorted_keys) and self.sorted_keys[idx] == pos:
                    self.sorted_keys.pop(idx)

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        pos = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, pos) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def get_n_nodes(self, key: str, n: int) -> list[str]:
        """Get n distinct nodes for replication (replica placement)."""
        if not self.ring or n > len(self._nodes):
            raise ValueError("Insufficient nodes")
        pos = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, pos) % len(self.sorted_keys)
        seen: set[str] = set()
        result: list[str] = []
        for i in range(len(self.sorted_keys)):
            node = self.ring[self.sorted_keys[(idx + i) % len(self.sorted_keys)]]
            if node not in seen:
                seen.add(node)
                result.append(node)
                if len(result) == n:
                    break
        return result

    def _hash(self, value: str) -> int:
        return int(hashlib.sha256(value.encode()).hexdigest(), 16)

    def distribution_stats(self, sample_keys: list[str]) -> dict[str, int]:
        """Check how evenly keys are distributed across nodes."""
        distribution: dict[str, int] = defaultdict(int)
        for key in sample_keys:
            node = self.get_node(key)
            if node:
                distribution[node] += 1
        return dict(distribution)

# Usage
ring = ConsistentHashRing(virtual_nodes=150)
ring.add_node("node-1")
ring.add_node("node-2")
ring.add_node("node-3")

# Check that adding node-4 moves ~25% of keys (not ~75%)
node = ring.get_node("some-user-id")
ring.add_node("node-4")
new_node = ring.get_node("some-user-id")
# If node != new_node, this key moved — expected for ~25% of keys
```

### Pattern: Raft Leader Election (Simplified State Machine)

```go
// Go — Raft node state machine (simplified, not production-ready)
package raft

import (
    "math/rand"
    "time"
)

type Role int
const (
    Follower  Role = iota
    Candidate
    Leader
)

type RaftNode struct {
    id          int
    role        Role
    currentTerm int
    votedFor    int  // -1 = no vote this term
    peers       []int
    votes       int

    // Channels for communication simulation
    heartbeat   chan struct{}
    requestVote chan VoteRequest
    voteResult  chan VoteResponse
}

func (n *RaftNode) run() {
    for {
        switch n.role {
        case Follower:
            // Random timeout: 150-300ms
            timeout := time.Duration(150+rand.Intn(150)) * time.Millisecond
            select {
            case <-n.heartbeat:
                // Reset timer — leader is alive
            case <-time.After(timeout):
                // No heartbeat — become candidate
                n.startElection()
            }

        case Candidate:
            // Waiting for vote responses
            select {
            case resp := <-n.voteResult:
                if resp.Term > n.currentTerm {
                    n.currentTerm = resp.Term
                    n.role = Follower  // Revert if higher term seen
                }
                if resp.VoteGranted {
                    n.votes++
                    if n.votes > len(n.peers)/2+1 {
                        n.role = Leader
                        n.sendHeartbeats()
                    }
                }
            case <-time.After(300 * time.Millisecond):
                // Election timeout — restart election with new term
                n.startElection()
            }

        case Leader:
            // Send heartbeats every 50ms to prevent follower elections
            time.Sleep(50 * time.Millisecond)
            n.sendHeartbeats()
        }
    }
}

func (n *RaftNode) startElection() {
    n.currentTerm++
    n.role = Candidate
    n.votedFor = n.id
    n.votes = 1  // Vote for self

    for _, peer := range n.peers {
        go n.requestVoteFrom(peer, VoteRequest{
            Term:        n.currentTerm,
            CandidateId: n.id,
        })
    }
}
```

### Pattern: Fencing Token for Safe Distributed Locks

The problem with lock TTL: GC pauses, clock skew, or process suspend can cause a process to hold a lock past its TTL. Another process acquires the lock. Now two processes believe they hold the lock.

Fencing tokens solve this: the lock service increments a monotonic token on each acquisition. Clients pass the token with every operation. The storage system rejects operations with a lower token than the last seen:

```java
// Lock service returns incrementing fencing token
public class FencedLock {
    private final AtomicLong tokenCounter = new AtomicLong(0);

    public LockAcquisition tryAcquire(String resource, Duration ttl) {
        // ... acquire lock logic ...
        return new LockAcquisition(resource, tokenCounter.incrementAndGet(), ttl);
    }
}

// Storage system enforces monotonic token
public class FencedStorage {
    private final ConcurrentHashMap<String, Long> lastTokenSeen = new ConcurrentHashMap<>();

    public void write(String key, Object value, long fencingToken) {
        long current = lastTokenSeen.getOrDefault(key, -1L);
        if (fencingToken <= current) {
            throw new StaleTokenException(
                "Fencing token " + fencingToken + " is stale (last seen: " + current + ")"
            );
        }
        lastTokenSeen.put(key, fencingToken);
        // ... perform write ...
    }
}

// Client: pass token with every operation
try (LockAcquisition lock = lockService.tryAcquire("inventory-update", Duration.ofSeconds(30))) {
    // Even if this process is delayed (GC, etc.) and lock expires on another node,
    // the fencing token prevents stale writes from succeeding
    storage.write("inventory:product-42", updatedInventory, lock.token());
}
```

### Pattern: SWIM Failure Detection (Gossip-based)

```
SWIM (Scalable Weakly-consistent Infection-style Membership Protocol):

1. Node A periodically pings a random peer B.
2. If B responds within timeout → B is alive.
3. If B does not respond:
   a. A selects k random nodes (C, D, E) and sends "ping-req B" messages.
   b. C, D, E each try to ping B directly.
   c. If any of C/D/E reach B → B is alive (A's connection to B is the problem).
   d. If none reach B within timeout → B is declared suspect.
4. Suspect nodes are given a grace period.
5. If suspect node does not send a self-update → declared dead.
6. Dead node info is gossiped to all nodes.

Benefits over heartbeat-to-coordinator:
- O(1) message load per node (constant, not proportional to cluster size)
- Resilient to coordinator failure
- Indirect probing reduces false positives from one-way connectivity issues
```

Used by: Hashicorp Consul (serf library), Cassandra (modified gossip), Kubernetes node heartbeat.

## Anti-Patterns

### Anti-Pattern: Using Wall-Clock Timestamps for Event Ordering

Two events on different nodes: Event A at `2024-01-01T10:00:00.001Z` (node 1), Event B at `2024-01-01T10:00:00.000Z` (node 2). Node 1's clock is 1ms ahead.

By wall-clock: A happened after B. By causal ordering: neither caused the other (concurrent events). Using wall-clock timestamps to determine event order is incorrect in distributed systems. Use Lamport clocks or vector clocks for causal ordering.

### Anti-Pattern: Assuming Network Calls are Fast

```java
// Holding a database transaction open while calling a remote service
@Transactional
public void processOrder(String orderId) {
    Order order = orderRepo.findById(orderId);  // DB connection held
    inventoryCheck = inventoryService.check(order.items());  // Remote call — could take 500ms+
    order.confirm();
    orderRepo.save(order);
}
```

The database connection is held open during the remote call. Under load with 100 concurrent requests, all database connections are held waiting for inventory service responses. If inventory service has elevated latency (500ms), 100 connections × 500ms = effective 50 connection-seconds consumed waiting. Connection pool exhaustion.

Fix: separate the remote call from the database transaction. Call inventory service, then open transaction, then persist.

### Anti-Pattern: Infinite Retry Without Jitter

All clients retry at exactly the same interval: T, 2T, 4T... If the server restarts at 4T, all clients wake up simultaneously at 4T and cause a thundering herd. The server crashes again.

Use full jitter: `sleep = random(0, base * 2^attempt)`. This spreads retries across the entire backoff window.

## References

- Ongaro, Diego, and John Ousterhout. "In Search of an Understandable Consensus Algorithm." USENIX ATC 2014. thesecretlivesofdata.com (visual Raft).
- Kleppmann, Martin. "How to do distributed locking." martin.kleppmann.com, 2016.
- Kleppmann, Martin. _Designing Data-Intensive Applications_. O'Reilly, 2017.
- Das, Abhinandan, et al. "SWIM: Scalable Weakly-consistent Infection-style Process Group Membership Protocol." DSN 2002.
- Karger, David, et al. "Consistent Hashing and Random Trees." ACM STOC 1997.
