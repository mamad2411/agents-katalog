# Caching Architecture, Invalidation & Resilience

## Purpose
Architect, implement, and audit multi-tiered caching systems (L1 in-process, L2 distributed, L3 edge/CDN) with strict consistency guarantees, deterministic invalidation protocols, mathematical eviction models (LRU, LFU, W-TinyLFU), singleflight deduplication, and robust defenses against cache stampede, penetration, breakdown, and avalanche.

## Use when
- Designing or implementing caching layers for high-throughput, low-latency microservices, APIs, and data access objects (DAOs).
- Preventing origin database saturation via request coalescing (SingleFlight), probabilistic early refresh (XFetch), or bloom filter admission.
- Implementing cache eviction policies (LRU, FIFO, LFU, ARC) with bounded memory limits.
- Defining cache invalidation lifecycles: Cache-Aside, Write-Through, Write-Behind, or CDC event-driven invalidation.
- Auditing caching strategies for stale reads, race conditions, memory leaks, and serialization overhead.

## Do not use when
- Managing single-variable concurrent memory synchronization without caching lifecycles (use `concurrency-quality`).
- Tuning raw database index layouts, query plans, or relational transaction isolation levels (use `database-review`).
- Measuring browser HTTP asset caching headers without server-side caching topologies (use `performance-web`).

## Required context
- Target read/write traffic ratios, peak QPS, and latency SLA targets (p50, p99, p99.9).
- Data volatility, staleness tolerance window ($\Delta t_{\text{stale}}$), and consistency requirements (strong vs eventual consistency).
- Memory budget constraints: RAM limits for L1 in-process heap and L2 distributed cache cluster (Redis, Memcached, Dragonfly).
- Network topology and origin database capacity limits.

## Procedure
1. **Define Caching Topology & Access Pattern**:
   - Select topology: L1 Local (in-process, sub-microsecond, zero serialization) + L2 Distributed (shared, sub-millisecond, cluster-wide consistency).
   - Select pattern:
     - **Cache-Aside (Lazy Loading)**: Read cache $\to$ on miss read DB $\to$ write cache. Ideal for read-heavy, irregular access.
     - **Write-Through**: Write to cache and DB synchronously. Guarantees cache consistency at write cost.
     - **Write-Behind (Write-Back)**: Acknowledge write after cache update; asynchronously drain batch to DB via write-ahead log.
2. **Dimension Capacity & Eviction Algorithms**:
   - Model hit ratio $H$ and effective latency:
     $$T_{\text{eff}} = H \cdot T_{\text{cache}} + (1 - H) \cdot T_{\text{origin}}$$
   - Enforce bounded memory ceilings. Select eviction policy:
     - **LRU (Least Recently Used)**: Standard general-purpose; $O(1)$ Hash Map + Doubly Linked List.
     - **W-TinyLFU**: High-efficiency frequency admission filter (Count-Min sketch) + Window LRU; optimal for skewed zipfian distributions.
3. **Mitigate Systemic Cache Hazards**:
   - **Cache Stampede (Thundering Herd)**: Enforce SingleFlight request coalescing so that concurrent misses for the same key make exactly one upstream call.
   - **Cache Avalanche**: Apply randomized uniform jitter to base TTL:
     $$\text{TTL}_{\text{actual}} = \text{TTL}_{\text{base}} \pm \text{Uniform}(0, J)$$
   - **Cache Penetration**: Guard against queries for non-existent entities using a Bloom Filter or caching sentinel empty values with short TTL ($30\text{s} - 60\text{s}$).
   - **Cache Breakdown**: Apply probabilistic early refresh (XFetch algorithm) for hot keys before actual expiration:
     $$\Delta \cdot \beta \cdot \ln(r) > \text{TTL}_{\text{remaining}}$$
4. **Implement Deterministic Invalidation & Ordering**:
   - In Cache-Aside architectures, always update the primary database *first*, commit the transaction, and *then* invalidate/evict the cache key.
   - For distributed deployments, leverage Transactional Outbox or Change Data Capture (CDC via Debezium/Kafka) to broadcast cache eviction events reliably.
5. **Enforce Serialization & Key Namespacing**:
   - Use deterministic, collision-resistant key schemas: `<service>:<entity>:<version>:<id>`.
   - Prefer efficient binary serialization (Protobuf, MessagePack, Cap'n Proto) over verbose JSON for high-throughput L2 caches.
6. **Verify Under High Concurrency**:
   - Subject the cache layer to simulated thundering herds ($1{,}000$ concurrent requests on a single cold key) and verify that origin DB receives exactly 1 query.
   - Run verification script `scripts/verify.sh` to confirm race freedom and eviction correctness.

## Decision rules
- **Never Unbounded**: All in-memory caches must have a strict capacity limit (max items or max memory bytes). Unbounded maps are prohibited.
- **SingleFlight Mandatory**: Any expensive origin fetch must be wrapped in a request coalescing primitive (e.g., `singleflight.Group`).
- **Post-Commit Eviction**: Invalidation must execute after the database transaction commits, never before or inside the uncommitted transaction.
- **TTL on All Keys**: Every cached item must have an explicit TTL. Permanent keys without TTL are forbidden in shared caches.
- **Fail-Open Graceful Degradation**: If the cache cluster becomes unavailable, the system must degrade gracefully (circuit breaker to origin with rate limiting) rather than crashing.

## Evidence required
- Caching architecture specification adhering to `templates/caching-strategy-spec.md`.
- Automated test logs demonstrating singleflight request suppression during stampedes.
- Eviction correctness and bounded memory tests under continuous insertion.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Caching specification document with key schemas, TTLs, and invalidation rules.
- Thread-safe, bounded cache implementation with singleflight coalescing.
- Automated tests proving stampede prevention and zero memory leaks.

## Stop conditions
- Complete caching layer implemented and verified against all 4 failure modes (Stampede, Avalanche, Penetration, Breakdown).
- Singleflight deduplication verified with $100\%$ origin query suppression for duplicate concurrent requests.
- Token budget exhausted.

## Escalation rules
- Escalate to Lead Architect if business requirements mandate zero-staleness strong consistency across distributed nodes (requires distributed locking or linearizable replication, not basic caching).
- Escalate to DBA if origin database cannot handle the p99 miss rate under degraded cache scenarios.
