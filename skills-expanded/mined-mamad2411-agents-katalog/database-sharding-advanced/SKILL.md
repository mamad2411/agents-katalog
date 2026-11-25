---
name: database-sharding-advanced
version: 1.0.0
min_mindforge_version: 10.1.1
status: stable
triggers: database sharding advanced, resharding without downtime, cross-shard query, shard key selection, hotspot mitigation, shard rebalancing, consistent hashing shard, virtual shard, shard routing, shard-nothing architecture, geographic sharding, shard split
compose: database-patterns
---

# Skill — Database Sharding (Advanced)

## When this skill activates
Any task involving horizontal database partitioning across multiple nodes,
shard key selection, hotspot mitigation, resharding without downtime,
cross-shard query strategies, or geographic data distribution.

## Mandatory actions when this skill is active

### Before writing any code
1. Confirm sharding is necessary (vertical scaling exhausted? read replicas insufficient?).
2. Select shard key using the three criteria: high cardinality + even distribution + query alignment.
3. Plan cross-shard query strategy for necessary joins/aggregations.
4. Design resharding approach (will need it eventually — plan now).

### During implementation
- Implement shard routing layer (application-level or proxy).
- Use consistent hashing with virtual nodes for even distribution.
- Denormalize data that would require frequent cross-shard joins.
- Pre-compute aggregations that span shards.
- Handle shard-local sequences (no global auto-increment).
- Implement request routing that is transparent to application code.

### After implementation
- Verify even distribution across shards (no hotspots).
- Test cross-shard queries perform within acceptable latency.
- Validate resharding procedure in staging (dual-write → migrate → verify → cut).
- Monitor per-shard metrics (query latency, storage, connections).
- Load test at 2x expected traffic to validate shard capacity.

## Shard Key Selection

### Three Criteria (All Must Be Met)
1. **High cardinality**: Many distinct values (user_id: good, country: bad).
2. **Even distribution**: Values spread evenly across shards (random UUID: good, sequential ID: bad for hash).
3. **Query alignment**: Most queries include the shard key (tenant_id if multi-tenant).

### Common Shard Keys
| Application Type | Good Shard Key | Why |
|-----------------|---------------|-----|
| Multi-tenant SaaS | tenant_id | All tenant data co-located |
| Social media | user_id | Profile + posts together |
| E-commerce | customer_id | Orders, cart, history together |
| IoT | device_id | Time-series per device |
| Gaming | player_id | Player state co-located |

### Anti-Pattern Shard Keys
- **Timestamp**: Creates hot shard (all writes to "current" shard).
- **Sequential ID**: Skews to latest shard.
- **Country/region**: Uneven (US shard overloaded, small countries under-utilized).
- **Status field**: Low cardinality, uneven distribution.

## Hotspot Mitigation

### Techniques
1. **Hash distribution**: Hash shard key before routing (spreads sequential keys).
2. **Virtual shards**: Map to many virtual shards, assign groups to physical nodes.
3. **Composite keys**: Combine shard key with secondary attribute (user_id + date_bucket).
4. **Time-based rotation**: For time-series, rotate shard assignment periodically.
5. **Write-behind aggregation**: Buffer hot-key writes, flush periodically.

### Detecting Hotspots
- Monitor per-shard write rate (>2x average = hotspot).
- Monitor per-shard storage growth (uneven = distribution problem).
- Monitor per-shard query latency (one slow = overloaded).

## Resharding Without Downtime

### The Double-Write Pattern
```
Phase 1: Dual-Write
  - Write to both old shard AND new shard.
  - Read from old shard.

Phase 2: Backfill
  - Copy historical data from old shard to new shard.
  - Continue dual-writing.

Phase 3: Verify
  - Compare old and new shard data (row counts, checksums).
  - Fix any discrepancies.

Phase 4: Cutover
  - Switch reads to new shard.
  - Continue dual-writing briefly (safety net).

Phase 5: Cleanup
  - Stop writing to old shard.
  - Archive/delete old shard data.
```

### Online Schema Change Tools
- **gh-ost** (GitHub): Trigger-free, replication-based.
- **pt-online-schema-change** (Percona): Trigger-based.
- **Spirit**: For MySQL resharding specifically.

### Rules
- Never do big-bang migration (all-at-once = risky).
- Always have rollback plan at every phase.
- Verify data integrity between phases (checksums).
- Run in staging first with production-like data volume.

## Cross-Shard Queries

### The Problem
Once data is sharded, joins across shards are expensive (scatter-gather).

### Strategies
| Strategy | When to Use | Trade-off |
|----------|-------------|-----------|
| Denormalization | Frequent joins | Storage cost, write complexity |
| Pre-computed aggregations | Analytics, dashboards | Staleness, compute cost |
| Scatter-gather | Rare queries | Latency, complexity |
| Global tables (replicated) | Small reference data | Replication lag |
| Application-level joins | Low-volume cross-shard | Code complexity |

### Denormalization Patterns
- Store user name alongside every order (avoid cross-shard user lookup).
- Embed category info in product documents.
- Maintain per-shard aggregation counters (updated async).

### When Scatter-Gather Is Acceptable
- Admin queries (not user-facing, latency tolerant).
- Batch jobs (run off-peak).
- Infrequent search queries (use dedicated search index instead).

## Consistent Hashing

### How It Works
1. Hash ring with positions 0 to 2^32.
2. Each physical node gets multiple virtual nodes (tokens) on the ring.
3. Data routes to first node clockwise from its hash position.
4. Adding/removing node only affects adjacent range.

### Virtual Nodes
- Each physical node owns 100-256 virtual nodes.
- More virtual nodes = more even distribution.
- Adding a physical node: assign new virtual nodes, migrate only affected ranges.
- Removing: redistribute its virtual nodes' ranges to neighbors.

### Benefits Over Simple Modulo
| Aspect | Modulo (hash % N) | Consistent Hashing |
|--------|-------------------|-------------------|
| Add node | ~100% data moves | ~1/N data moves |
| Remove node | ~100% data moves | ~1/N data moves |
| Distribution | Depends on hash | Even with virtual nodes |
| Complexity | Simple | Moderate |

## Geographic Sharding

### Use Cases
- Data sovereignty (EU data stays in EU).
- Latency optimization (users read from nearest region).
- Regulatory compliance (GDPR, data residency laws).

### Patterns
| Pattern | Reads | Writes | Consistency |
|---------|-------|--------|-------------|
| Write-local, read-local | Fast | Fast | Eventual (per-region) |
| Write-primary, read-any | Fast | Slower (cross-region) | Strong for writes |
| Multi-writer | Fast | Fast | Conflict resolution needed |

### Conflict Resolution (Multi-Writer)
- Last-write-wins (simple, data loss possible).
- CRDTs (conflict-free, limited data types).
- Application-level merge (complex, most flexible).
- Operational transforms (collaborative editing).

## Shard Routing

### Routing Approaches
1. **Application-level**: App knows shard map, routes directly.
2. **Proxy layer**: Middleware (Vitess, ProxySQL) routes transparently.
3. **Client library**: SDK handles routing, app unaware.

### Shard Map
```json
{
  "shards": [
    {"id": 0, "range": "0000-3FFF", "host": "db-shard-0.internal"},
    {"id": 1, "range": "4000-7FFF", "host": "db-shard-1.internal"},
    {"id": 2, "range": "8000-BFFF", "host": "db-shard-2.internal"},
    {"id": 3, "range": "C000-FFFF", "host": "db-shard-3.internal"}
  ]
}
```

## Self-check
- [ ] Shard key meets all three criteria (cardinality, distribution, query alignment).
- [ ] No hotspots detected (per-shard metrics balanced).
- [ ] Cross-shard query strategy defined (denormalize, pre-compute, or scatter-gather).
- [ ] Resharding procedure documented and tested in staging.
- [ ] Consistent hashing with virtual nodes for even distribution.
- [ ] Application transparent to sharding (routing layer handles it).
- [ ] Per-shard monitoring (latency, storage, connections).
- [ ] Rollback plan exists at every migration phase.
- [ ] Geographic compliance verified if required.
