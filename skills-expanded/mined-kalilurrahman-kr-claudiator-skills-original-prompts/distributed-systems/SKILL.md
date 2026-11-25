---
name: distributed-systems
description: Design distributed systems with consensus algorithms, partitioning, and eventual consistency. Outputs system architecture, CAP trade-offs, and failure handling.
argument-hint: [system scale, consistency requirements, partition tolerance]
allowed-tools: Read, Write, Bash
---

# Distributed Systems Design

Design systems that span multiple servers/datacenters. Not single-server apps — distributed consensus, partitioning strategies, and managing network failures.

## Process

1. **Choose CAP trade-offs.** Consistency, Availability, Partition tolerance (pick 2).
2. **Design partitioning.** Horizontal sharding, consistent hashing.
3. **Select consensus algorithm.** Paxos, Raft, or leaderless replication.
4. **Handle failures.** Network partitions, node crashes, split-brain.
5. **Implement replication.** Leader-follower, multi-master, quorum-based.
6. **Manage distributed state.** Distributed transactions, eventual consistency.
7. **Monitor system health.** Cluster status, replication lag, partition detection.

## Output Format

### Distributed System: [Application]

**Architecture:** Multi-datacenter, 3 regions  
**CAP Choice:** AP (Available + Partition-tolerant)  
**Consistency:** Eventual consistency (< 100ms)  
**Partitioning:** Consistent hashing across 16 shards  
**Consensus:** Raft for leader election

---

## CAP Theorem

**You can only pick 2 of 3:**

```
      Consistency (C)
          /\
         /  \
        /    \
       /      \
      /   CA   \
     /__________\
    /            \
   / CP        AP \
  /________________\
Partition      Availability
Tolerance (P)      (A)
```

### CA: Consistency + Availability
- **No partition tolerance**
- Single datacenter only
- Example: Traditional RDBMS (PostgreSQL, MySQL)

### CP: Consistency + Partition tolerance
- **No availability during partition**
- Strong consistency guaranteed
- Example: HBase, MongoDB (with majority write concern)

### AP: Availability + Partition tolerance
- **No strong consistency**
- Eventually consistent
- Example: Cassandra, DynamoDB, Riak

**In practice:** Network partitions happen, so choose between CP or AP.

---

## Partitioning Strategies

### Range-Based Partitioning

```
Partition 1: A-F
Partition 2: G-M
Partition 3: N-S
Partition 4: T-Z

Pros: Range queries efficient
Cons: Hot spots (uneven distribution)
```

### Hash-Based Partitioning

```
hash(key) % num_partitions

user_123 → hash(123) % 4 = 3 → Partition 3
user_456 → hash(456) % 4 = 0 → Partition 0

Pros: Even distribution
Cons: Range queries require scatter-gather
```

### Consistent Hashing

```
                Node C (hash: 800)
                      ●
                     /
                    /
    Node A ●-------●------- Ring (0-1023)
    (200)          \
                    \
                     ●
                Node B (hash: 500)

Key placement:
- key_100 → Node A (closest clockwise)
- key_600 → Node C
- key_300 → Node B

Add Node D (hash: 350):
- Only keys 300-350 move from B to D
- Minimal redistribution
```

**Implementation:**
```python
import hashlib

class ConsistentHash:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas  # Virtual nodes per physical node
        self.ring = {}
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        """Add node with virtual nodes"""
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_key = self._hash(virtual_key)
            self.ring[hash_key] = node
            self.sorted_keys.append(hash_key)
        
        self.sorted_keys.sort()
    
    def remove_node(self, node):
        """Remove node"""
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_key = self._hash(virtual_key)
            del self.ring[hash_key]
            self.sorted_keys.remove(hash_key)
    
    def get_node(self, key):
        """Find node for key"""
        if not self.ring:
            return None
        
        hash_key = self._hash(key)
        
        # Find first node clockwise
        for ring_key in self.sorted_keys:
            if hash_key <= ring_key:
                return self.ring[ring_key]
        
        # Wrap around
        return self.ring[self.sorted_keys[0]]

# Usage
ch = ConsistentHash(['node1', 'node2', 'node3'])

print(ch.get_node('user_123'))  # node2
print(ch.get_node('user_456'))  # node1

# Add node (minimal redistribution)
ch.add_node('node4')
```

---

## Consensus Algorithms

### Raft (Leader-Based)

```
State machine:
Follower → Candidate → Leader

Election:
1. Follower times out (no heartbeat from leader)
2. Becomes Candidate, requests votes
3. If majority votes received, becomes Leader
4. Leader sends heartbeats to maintain authority

Log replication:
1. Client sends command to Leader
2. Leader appends to own log
3. Leader sends AppendEntries to Followers
4. Once majority replicated, Leader commits
5. Leader notifies Followers to commit
```

**Raft implementation (etcd):**
```go
// Client write
client := clientv3.New(clientv3.Config{
    Endpoints: []string{"http://localhost:2379"},
})

// Write to cluster (requires leader)
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
_, err := client.Put(ctx, "key", "value")
defer cancel()

// Read (can be from follower with stale data or leader for consistency)
resp, err := client.Get(ctx, "key")
```

### Paxos (More General)

```
Roles: Proposer, Acceptor, Learner

Phase 1 (Prepare):
- Proposer sends proposal number to Acceptors
- Acceptors promise not to accept lower proposals

Phase 2 (Accept):
- Proposer sends value to Acceptors
- If majority accepts, value is chosen

Difficult to implement, Raft more practical
```

### Leaderless Replication (Quorum)

```
W + R > N
W: Write quorum
R: Read quorum  
N: Total replicas

Example: N=3, W=2, R=2
- Write to 2 nodes (majority)
- Read from 2 nodes (majority)
- Guaranteed to read latest write

Cassandra tunable consistency:
- W=1, R=1: Fast, low consistency
- W=QUORUM, R=QUORUM: Balanced
- W=ALL, R=ONE: Strong consistency writes
```

---

## Replication Patterns

### Leader-Follower (Primary-Replica)

```
┌────────┐
│ Leader │ ← Writes
└───┬────┘
    │ Replicate
    ├─────────┬─────────┐
    ▼         ▼         ▼
┌────────┐┌────────┐┌────────┐
│Follower││Follower││Follower│ ← Reads
└────────┘└────────┘└────────┘

Pros: Simple, consistent reads from leader
Cons: Leader bottleneck, failover needed
```

**PostgreSQL streaming replication:**
```sql
-- Primary
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- Replica
CREATE SUBSCRIPTION my_subscription
    CONNECTION 'host=primary.example.com port=5432 dbname=mydb'
    PUBLICATION my_publication;
```

### Multi-Master (Multi-Leader)

```
┌────────┐      ┌────────┐
│Master A│◄────►│Master B│
└────┬───┘      └───┬────┘
     │              │
     └──────┬───────┘
            ▼
    Conflict resolution

Pros: No single point of failure
Cons: Conflict resolution complex
```

**Conflict resolution strategies:**
```
Last Write Wins (LWW):
- Each write has timestamp
- Latest timestamp wins
- Data loss possible

Vector Clocks:
- Track causality
- Detect concurrent writes
- Require manual resolution

CRDTs (Conflict-free Replicated Data Types):
- Mathematically guaranteed convergence
- No conflicts by design
```

---

## Distributed Transactions

### Two-Phase Commit (2PC)

```
Phase 1: Prepare
Coordinator → All participants: "Can you commit?"
Participants → Coordinator: "Yes" or "No"

Phase 2: Commit
If all "Yes":
  Coordinator → All: "Commit"
Else:
  Coordinator → All: "Abort"

Problem: Coordinator is single point of failure
```

### Saga Pattern (Compensating Transactions)

```
Order → Payment → Inventory → Shipping

If Inventory fails:
- Compensate Payment (refund)
- Compensate Order (cancel)

Each service has forward transaction + compensating transaction
```

```python
# Saga orchestrator
class OrderSaga:
    def execute(self, order):
        try:
            # Create order
            order_id = order_service.create(order)
            
            # Charge payment
            payment_id = payment_service.charge(order.amount)
            
            # Reserve inventory
            inventory_id = inventory_service.reserve(order.items)
            
            # Ship
            shipping_id = shipping_service.ship(order)
            
            return {'success': True, 'order_id': order_id}
        
        except InventoryError:
            # Compensate payment
            payment_service.refund(payment_id)
            # Compensate order
            order_service.cancel(order_id)
            
            return {'success': False, 'error': 'Out of stock'}
```

---

## Vector Clocks

```python
class VectorClock:
    """Track causality in distributed systems"""
    
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = {}
    
    def increment(self):
        """Increment own clock"""
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1
    
    def update(self, other_clock):
        """Merge with received clock"""
        for node, count in other_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), count)
        self.increment()
    
    def happens_before(self, other):
        """Check if this event happened before other"""
        return (all(self.clock.get(k, 0) <= other.get(k, 0) for k in self.clock) and
                any(self.clock.get(k, 0) < other.get(k, 0) for k in self.clock))
    
    def concurrent(self, other):
        """Check if events are concurrent"""
        return not self.happens_before(other) and not other.happens_before(self.clock)

# Usage
# Node A
clock_a = VectorClock('A')
clock_a.increment()  # {A: 1}

# Node B receives message
clock_b = VectorClock('B')
clock_b.update(clock_a.clock)  # {A: 1, B: 1}

# Concurrent writes detected
if clock_a.concurrent(clock_b.clock):
    print("Conflict: concurrent writes")
```

---

## Split-Brain Prevention

```
Network partition:
┌────────┐       ┌────────┐
│ Node A │  ╳    │ Node B │
│ Node C │       │ Node D │
└────────┘       └────────┘

Both sides think they're the cluster
Both try to become leader → Split-brain

Solution: Quorum
- Require majority (3 out of 5 nodes)
- Only side with majority can elect leader
```

**ZooKeeper quorum:**
```properties
# zookeeper.properties
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181

# Cluster configuration
server.1=zk1:2888:3888
server.2=zk2:2888:3888
server.3=zk3:2888:3888
server.4=zk4:2888:3888
server.5=zk5:2888:3888

# Requires 3/5 for quorum
```

---

## Gossip Protocol

```python
import random
import time

class GossipNode:
    """Epidemic-style information dissemination"""
    
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.data = {}
        self.version = {}
    
    def update(self, key, value):
        """Update local data"""
        self.data[key] = value
        self.version[key] = time.time()
    
    def gossip(self):
        """Periodically share state with random peer"""
        if not self.peers:
            return
        
        # Pick random peer
        peer = random.choice(self.peers)
        
        # Send state
        peer_data, peer_version = peer.receive_gossip(self.data, self.version)
        
        # Merge peer state
        for key, value in peer_data.items():
            if key not in self.version or peer_version[key] > self.version[key]:
                self.data[key] = value
                self.version[key] = peer_version[key]
    
    def receive_gossip(self, data, version):
        """Receive gossip from peer"""
        for key, value in data.items():
            if key not in self.version or version[key] > self.version[key]:
                self.data[key] = value
                self.version[key] = version[key]
        
        return self.data, self.version
```

**Use cases:**
- Cassandra: Node membership
- Consul: Service discovery
- Redis Cluster: Cluster state

---

## Distributed Monitoring

```python
from prometheus_client import Gauge, Counter

# Cluster health
cluster_nodes_total = Gauge(
    'cluster_nodes_total',
    'Total nodes in cluster',
    ['status']  # healthy, unhealthy
)

cluster_partitions = Gauge(
    'cluster_partitions',
    'Number of network partitions detected'
)

consensus_leader_changes = Counter(
    'consensus_leader_changes_total',
    'Total leader elections'
)

replication_lag_seconds = Gauge(
    'replication_lag_seconds',
    'Replication lag in seconds',
    ['follower_id']
)
```

**Alerts:**
```yaml
- alert: ClusterSplitBrain
  expr: cluster_partitions > 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "Network partition detected"

- alert: HighReplicationLag
  expr: replication_lag_seconds > 10
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Follower {{ $labels.follower_id }} lagging by {{ $value }}s"
```

## Rules

- CAP theorem: choose 2 of 3 — partition tolerance required for distributed systems, pick consistency or availability.
- Quorum-based writes prevent split-brain — W + R > N guarantees overlap.
- Consistent hashing minimizes reshuffling — adding node only moves 1/N data, not everything.
- Leader-based replication for strong consistency — all writes through leader ensures ordering.
- Leaderless for availability — no single point of failure, survives any node death.
- Vector clocks detect concurrent writes — timestamps alone miss causality.
- Sagas for distributed transactions — 2PC blocks on coordinator failure, sagas compensate.
- Gossip for membership — epidemic spread ensures eventual convergence.
- Monitor replication lag — lag > 10s indicates network/performance issues.
- Test partition tolerance — chaos engineering kills nodes, partitions network to verify resilience.
