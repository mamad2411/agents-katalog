---
name: "consistency-patterns"
description: "Consistency patterns with code: G-Counter and OR-Set CRDTs, read-your-writes session tokens, Cassandra quorum settings, and vector clock conflict detection, plus anti-patterns such as 2PC across microservices. Use when choosing or implementing a consistency model."
---

# Data Consistency Patterns

> Named patterns with code for CRDT implementations, vector clock comparison, quorum configuration, 2PC protocol, read-your-writes consistency, and anti-entropy.

## Patterns

### Pattern: G-Counter CRDT (Distributed Like Counter)

```python
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class GCounter:
    """
    Grow-only counter CRDT. Safe for concurrent increments from multiple nodes.
    Example: distributed like counter, page view counter.
    """
    node_id: str
    counts: Dict[str, int] = field(default_factory=dict)

    def increment(self, by: int = 1) -> None:
        self.counts[self.node_id] = self.counts.get(self.node_id, 0) + by

    @property
    def value(self) -> int:
        return sum(self.counts.values())

    def merge(self, other: 'GCounter') -> 'GCounter':
        """
        Merge: max of each node's count.
        Properties: commutative, associative, idempotent = CRDT.
        """
        all_nodes = set(self.counts) | set(other.counts)
        merged = GCounter(self.node_id)
        for node in all_nodes:
            merged.counts[node] = max(
                self.counts.get(node, 0),
                other.counts.get(node, 0)
            )
        return merged

    def to_dict(self) -> dict:
        return {'node_id': self.node_id, 'counts': self.counts}

    @classmethod
    def from_dict(cls, data: dict) -> 'GCounter':
        c = cls(data['node_id'])
        c.counts = data['counts']
        return c

# Usage: two nodes independently increment, then merge
node1 = GCounter('node-1')
node2 = GCounter('node-2')

node1.increment(5)
node2.increment(3)
node1.increment(2)  # Concurrent with node2

# Merge — result is 10, regardless of merge order (commutative)
merged = node1.merge(node2)
assert merged.value == 10  # 7 (node1) + 3 (node2)
```

### Pattern: OR-Set CRDT (Concurrent Add/Remove)

```python
import uuid
from dataclasses import dataclass, field
from typing import Set, Tuple

@dataclass
class ORSet:
    """
    Observed-Remove Set. Supports concurrent add and remove without conflicts.
    Each add is tagged with a unique ID. Remove removes the specific add instance.
    Example: collaborative shopping cart, team member list.
    """
    # (element, unique_tag) pairs
    adds: Set[Tuple[str, str]] = field(default_factory=set)
    removes: Set[Tuple[str, str]] = field(default_factory=set)

    def add(self, element: str) -> None:
        tag = str(uuid.uuid4())
        self.adds.add((element, tag))

    def remove(self, element: str) -> None:
        # Remove all current instances of this element
        to_remove = {(e, t) for e, t in self.adds if e == element}
        self.removes.update(to_remove)

    @property
    def elements(self) -> Set[str]:
        effective = self.adds - self.removes
        return {e for e, _ in effective}

    def merge(self, other: 'ORSet') -> 'ORSet':
        merged = ORSet()
        merged.adds = self.adds | other.adds
        merged.removes = self.removes | other.removes
        return merged

# Concurrent add and remove converge correctly
cart1 = ORSet()
cart2 = ORSet()

cart1.add("product-A")  # Both nodes have product-A

# Concurrent: cart1 removes, cart2 adds another instance
cart1.remove("product-A")
cart2.add("product-A")  # New add with new tag

merged = cart1.merge(cart2)
# cart2's add (new tag) survives. cart1's remove only removed cart1's specific add.
assert "product-A" in merged.elements
```

### Pattern: Read-Your-Writes Consistency (Session Token)

After a write, route subsequent reads to the primary for a brief window, or pass a read token that guarantees the read reflects at least that write position:

```typescript
// Session-based read-your-writes consistency
interface WriteResult {
  data: unknown;
  replicationPosition: string;  // WAL LSN or Kafka offset
}

class ConsistentOrderService {
  private readonly writeDb: DatabaseClient;
  private readonly readDb: DatabaseClient;

  async placeOrder(request: PlaceOrderRequest): Promise<Order> {
    // Write to primary
    const result: WriteResult = await this.writeDb.insert('orders', request);

    // Store replication position in session (Redis or cookie)
    await this.sessionStore.set(
      `ryw:${request.userId}`,
      result.replicationPosition,
      300  // TTL: 5 minutes
    );

    return result.data as Order;
  }

  async getOrders(userId: string): Promise<Order[]> {
    // Check if user has a recent write position
    const requiredPosition = await this.sessionStore.get(`ryw:${userId}`);

    if (requiredPosition) {
      // Check if replica has caught up to the write position
      const replicaPosition = await this.readDb.getReplicationPosition();
      if (replicaPosition >= requiredPosition) {
        return this.readDb.query('SELECT * FROM orders WHERE user_id = $1', [userId]);
      }
      // Replica hasn't caught up — read from primary
      return this.writeDb.query('SELECT * FROM orders WHERE user_id = $1', [userId]);
    }

    // No recent write — safe to read from replica
    return this.readDb.query('SELECT * FROM orders WHERE user_id = $1', [userId]);
  }
}
```

### Pattern: Quorum Configuration (Cassandra)

```python
# Cassandra consistency level selection
# N=3 replicas, RF=3

CONSISTENCY_SCENARIOS = {
    "strong_consistency": {
        "write": "QUORUM",   # W=2 (RF/2 + 1)
        "read": "QUORUM",    # R=2
        # R + W = 4 > N = 3 → guaranteed overlap → linearizable
        "latency": "higher", "availability": "lower"
    },
    "eventual_consistency": {
        "write": "ONE",      # W=1
        "read": "ONE",       # R=1
        # R + W = 2 ≤ N = 3 → possible stale read
        "latency": "lowest", "availability": "highest"
    },
    "local_consistency": {
        # Multi-datacenter: enforce quorum within local DC only
        "write": "LOCAL_QUORUM",
        "read": "LOCAL_QUORUM",
        # Avoids cross-DC latency while maintaining consistency within DC
        "latency": "medium", "availability": "medium"
    },
}
```

Cassandra CQL for consistency per operation:
```sql
-- Strong consistency for financial balance read
SELECT balance FROM accounts WHERE id = ? WITH CONSISTENCY QUORUM;

-- Eventual consistency for product view count (high write rate, minor inconsistency OK)
UPDATE product_views SET views = views + 1 WHERE id = ? WITH CONSISTENCY ONE;
```

### Pattern: Conflict Detection with Vector Clocks

```java
public class VectorClockConflictDetector {

    public ConflictResult detectConflict(VersionedValue v1, VersionedValue v2) {
        VectorClock vc1 = v1.vectorClock();
        VectorClock vc2 = v2.vectorClock();

        if (vc1.happensBefore(vc2)) {
            return ConflictResult.NO_CONFLICT_V2_WINS;
        } else if (vc2.happensBefore(vc1)) {
            return ConflictResult.NO_CONFLICT_V1_WINS;
        } else {
            // Neither precedes the other — concurrent writes — CONFLICT
            return ConflictResult.CONFLICT_REQUIRES_RESOLUTION;
        }
    }

    public VersionedValue resolve(VersionedValue v1, VersionedValue v2, ConflictResolution strategy) {
        return switch (strategy) {
            case LAST_WRITE_WINS -> v1.timestamp().isAfter(v2.timestamp()) ? v1 : v2;
            case MERGE -> new VersionedValue(mergeValues(v1.value(), v2.value()),
                                            v1.vectorClock().merge(v2.vectorClock()),
                                            Instant.now());
            case PRESENT_TO_USER -> throw new ConflictException(v1, v2);
        };
    }
}
```

## Anti-Patterns

### Anti-Pattern: Assuming Eventual Consistency Means "Will Be Consistent Soon"

Eventual consistency guarantees convergence eventually — but "eventually" has no time bound. In practice, replication lag in well-operated systems is milliseconds to seconds. But under load, during network issues, or with slow consumers, "eventually" can be minutes or hours.

Do not build user-facing features on eventual consistency without handling the inconsistency window. The user who updates their profile and immediately sees the old value is experiencing eventual consistency without read-your-writes guarantee.

### Anti-Pattern: Using 2PC Across Microservices

Two-phase commit blocks both participants during the coordinator decision window. If the coordinator crashes after sending PREPARE, participants are locked until the coordinator recovers. In a microservices architecture with multiple teams and independent deployment, this creates tight availability coupling.

Use the Saga pattern instead: each service executes a local transaction, publishes an event, and defines a compensating transaction. No coordinator, no blocking.

### Anti-Pattern: Ignoring Clock Skew in LWW Conflict Resolution

Last-Write-Wins (LWW) with wall-clock timestamps assumes clocks are synchronized. In distributed systems, NTP keeps clocks within ~1ms of each other — but during partitions or cloud instance time jumps, clock skew can be seconds.

If two writes happen within the clock skew window, LWW may "win" with the wrong value. For LWW to be safe: use logical timestamps (Lamport clocks), or hybrid logical clocks (HLC, Kulkarni et al., 2014), or vector clocks.

### Anti-Pattern: Strong Consistency for Everything

Using linearizable consistency (Zookeeper, etcd, global SQL transactions) for all reads and writes, including non-critical data like product view counts, recommendation impressions, and social feed updates. Every operation pays the coordination overhead (consensus round = multiple network round-trips).

Classify data by consistency requirement: financial balances require linearizability; product catalog requires read-your-writes; analytics counters accept eventual consistency. Apply the appropriate guarantee to each.

## References

- Brewer, Eric. "Towards Robust Distributed Systems." SOSP, 2000.
- Kleppmann, Martin. _Designing Data-Intensive Applications_. O'Reilly, 2017. Chapter 9.
- Shapiro, Marc, et al. "Conflict-free Replicated Data Types." INRIA 2011.
- DeCandia, Giuseppe, et al. "Dynamo: Amazon's Highly Available Key-value Store." SOSP 2007.
- Lamport, Leslie. "Time, Clocks, and the Ordering of Events." CACM 1978.
- Apache Cassandra documentation: cassandra.apache.org/doc/latest/consistency.html.
