---
name: scalability-and-performance
description: >
  Scale systems and cut latency. Use when designing for growth, handling
  read-heavy or write-heavy traffic, high latency, slow queries, 10x traffic
  spikes, choosing vertical vs horizontal scaling, partitioning, load balancing
  algorithms, or optimizing throughput and response time.
---

# Scalability and Performance

Make the system handle more load and answer faster without a rewrite.

## When to use
- Traffic growing; something is about to become the bottleneck.
- Read-heavy, write-heavy, or spiky workloads.
- High latency, slow endpoints, slow queries.
- Choosing a scaling or partitioning strategy.

## Scaling framework
1. **Measure first.** Find the actual bottleneck (CPU, memory, IO, DB, network,
   lock). Never optimize blind. See `observability`.
2. **Scale up (vertical)** when simple and cost allows: more CPU/RAM.
3. **Scale out (horizontal)** for durability and elastic capacity: more nodes.
4. **Decouple** hot paths with async queues and caches.
5. **Partition** data when a single node can no longer hold/serve it.

## Playbook by symptom
| Symptom | Move |
|---|---|
| Read-heavy | Caching, read replicas, CDN, denormalize |
| Write-heavy | Async workers, LSM-tree store, queue, sharding by key |
| High latency | CDN, edge, cache, connection pooling, fewer round trips |
| Slow queries | Indexes, query rewrite, sharding, materialized views |
| Spiky traffic | Autoscaling, queue + workers, load shedding, rate limits |
| Single node limit | Shard/partition horizontally, consistent hashing |

## Partitioning & load distribution
- Vertical vs horizontal partitioning; sharding algorithms (range, hash,
  consistent hashing, directory-based).
- Load balancing algorithms: round robin, least connections, least response
  time, IP hash, weighted, consistent hashing.
- Watch for hotspots and rebalancing cost.

## Checklist
- [ ] Bottleneck measured, not guessed.
- [ ] Stateless services where possible (scale-out friendly).
- [ ] Cache + CDN on hot read paths.
- [ ] Async for non-critical writes.
- [ ] Partition key chosen to avoid hotspots.
- [ ] Autoscaling + rate limiting + backpressure.
- [ ] Load test at expected peak and 2-3x.

## Common pitfalls
- Scaling before measuring.
- Stateful services blocking horizontal scale.
- Sharding without a rebalancing plan.
- Caching without invalidation strategy.
- Ignoring tail latency (p99), optimizing only the average.

## References
- `...\8-must-know-scalability-strategies.md`
- `...\a-crash-course-on-architectural-scalability.md`
- `...\how-to-scale-a-website-to-support-millions-of-users.md`
- `...\top-5-strategies-to-reduce-latency.md`
- `...\top-6-load-balancing-algorithms.md`
- `...\vertical-partitioning-vs-horizontal-partitioning.md`
- `...\top-5-common-ways-to-improve-api-performance.md`
- `...\which-latency-numbers-should-you-know.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`system-design-method`, `caching-and-cdn`, `database-design`,
`observability`, `high-availability-and-resilience`.
