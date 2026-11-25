---
name: distributed-consensus-reliability
description: >-
  Reason about distributed consensus for reliability: when to use Paxos/Raft style systems, failure modes, and operational risks from Google SRE. Use when designing strongly consistent control planes or debugging quorum pain.
---

# Distributed Consensus Reliability

**Domain:** `resilience`  
**Sources:** SRE Book 1e Ch23

## When to use

- Choosing consensus-backed storage/coordination
- Quorum outages / leader flaps
- Control-plane reliability reviews

## Principles

- Consensus is powerful and operationally expensive — use where consistency is required.
- Quorum membership, latency, and network partitions dominate reliability.
- Separate control plane consensus from bulk data path when possible.
- Observe leader changes, commit latency, and peer health.

## Workflow

1. Confirm consistency requirement vs eventual OK.
2. Size quorum and failure tolerance (e.g. 2f+1).
3. Place members across failure domains carefully.
4. Define backup/restore and membership-change runbooks.
5. Alert on quorum risk, not only process down.

## Decision guide

- If cross-region sync latency breaks SLOs → rethink topology or consistency.

## Output template

```markdown
# Consensus reliability review
- Why consensus:
- Topology / failure tolerance:
- Observed risks:
- Runbooks:
```

## Anti-patterns

- Using ZooKeeper/etcd for huge data.
- Single-region quorum for multi-region hard needs.

## Related skills

`data-integrity`, `designing-for-resilience`

## Canonical references

- [Distributed Consensus](https://sre.google/sre-book/managing-critical-state/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
