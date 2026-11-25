---
name: distributed-systems-multi-region-data-topology
description: "Residency, replication lag, failover semantics, and write-conflict strategy before the second region exists."
---
# Design multi-region data topologies honestly

> Residency, replication lag, failover semantics, and write-conflict strategy before the second region exists.

**Track:** ⚙️ Backend Engineering · **Domain:** Distributed Systems · **Level:** advanced · **~50 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Residency, replication lag, failover semantics, and write-conflict strategy before the second region exists.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Map residency requirements per dataset BEFORE topology; law constrains design
2. Pick write topology: single-primary simplicity vs multi-primary conflict reality
3. Model cross-region latency into user journeys region-by-region
4. Define failover triggers, RTO/RPO per tier, and split-brain prevention mechanism
5. Rehearse regional evacuation with production-scale data annually
6. Instrument per-region error/latency separately; averages hide one dead region

## Common Pitfalls

- Multi-primary chosen then conflicts resolved by whoever writes last
- Failover tested with empty databases only

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill distributed-systems-multi-region-data-topology
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill distributed-systems-multi-region-data-topology -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills