---
name: distributed-systems-consistency-model-selection
description: "Strong vs bounded-staleness vs eventual mapped to business harm scenarios, not fashion."
---
# Choose consistency models per data class deliberately

> Strong vs bounded-staleness vs eventual mapped to business harm scenarios, not fashion.

**Track:** ⚙️ Backend Engineering · **Domain:** Distributed Systems · **Level:** advanced · **~45 min**

**Who this is for:** Backend Engineers, API Developers, Platform Engineers, Full-Stack Developers

## When to Use This Skill

Strong vs bounded-staleness vs eventual mapped to business harm scenarios, not fashion.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. List data classes with concrete stale-read harm examples in money terms
2. Default everything eventual; upgrade ONLY classes failing the harm test
3. For upgrades prefer session/bounded-staleness before paying strong-consistency latency
4. Document chosen model per entity in architecture decision records
5. Design compensations for eventual paths (idempotent corrections, reconciliation)
6. Test partition behavior deliberately; verify degraded modes match documentation

## Common Pitfalls

- Strong consistency everywhere 'for safety', latency budgets destroyed
- Eventual everywhere 'for scale', double-charges discovered by finance

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill distributed-systems-consistency-model-selection
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill distributed-systems-consistency-model-selection -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills