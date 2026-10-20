---
name: high-availability-and-resilience
description: >
  Design systems that survive failure. Use for high availability, fault
  tolerance, redundancy, failover, disaster recovery (RTO/RPO), retries with
  backoff, idempotency, circuit breakers, bulkheads, distributed locks, node
  failure detection, and eliminating single points of failure.
---

# High Availability and Resilience

Assume everything fails. Design so failures are contained, detected, and
recovered automatically.

## When to use
- Designing for uptime SLAs / SLOs.
- Removing single points of failure.
- Handling transient errors, retries, partial failures.
- Planning backups, disaster recovery, multi-region.

## Core principles
1. **Redundancy.** No single instance is load-bearing. Replicate services, DBs,
   zones.
2. **Failover.** Automatic promotion of healthy replicas; health checks +
   leader election.
3. **Isolation.** Bulkheads so one failing dependency does not sink everything.
4. **Graceful degradation.** Serve stale/partial results instead of erroring.
5. **Idempotency.** Safe retries require idempotent operations.
6. **Observability.** Detect failure fast (heartbeats, health checks, alerts).

## Resilience patterns
- Retry with exponential backoff + jitter; cap retries.
- Circuit breaker (closed → open → half-open).
- Bulkhead, timeout, load shedding, rate limiting.
- Idempotency keys for writes and payments.
- Outbox / saga for distributed transactions.
- Distributed lock (lease-based) for coordination.
- Heartbeat + gossip for node failure detection.

## Backup & DR
- Define **RTO** (max downtime) and **RPO** (max data loss) first.
- Strategies: backup & restore, pilot light, warm standby, active-active.
- Test restores; an untested backup is not a backup.

## Checklist
- [ ] Every component redundant or explicitly accepted as SPOF.
- [ ] Health checks + automated failover.
- [ ] Retries idempotent, bounded, with backoff.
- [ ] Circuit breakers + timeouts on all remote calls.
- [ ] Backpressure / load shedding under overload.
- [ ] RTO/RPO defined; DR strategy matches them.
- [ ] Chaos/failure testing performed.

## Common pitfalls
- Retrying non-idempotent writes (double payments).
- Timeouts longer than the caller's patience (cascading stalls).
- Retry storms amplifying an outage.
- Backups never restored/tested.
- Multi-region with no conflict resolution plan.

## References
- `...\a-cheat-sheet-for-designing-fault-tolerant-systems.md`
- `...\resiliency-patterns.md`
- `...\cloud-disaster-recovery-strategies.md`
- `...\how-do-we-design-for-high-availability.md`
- `...\how-do-we-retry-on-failures.md`
- `...\top-6-cases-to-apply-idempotency.md`
- `...\how-do-we-detect-node-failures-in-distributed-systems.md`
- `...\why-do-we-need-to-use-a-distributed-lock.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`distributed-systems`, `scalability-and-performance`, `observability`,
`messaging-and-streaming`.
