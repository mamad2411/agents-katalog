---
name: detection-operations-threat-intel-operationalization
description: "Relevance filtering, indicator decay, and hunt/detection integration converting feeds into actions."
---
# Operationalize threat intel instead of hoarding it

> Relevance filtering, indicator decay, and hunt/detection integration converting feeds into actions.

**Track:** 🔐 Cybersecurity · **Domain:** Detection Operations · **Level:** advanced · **~40 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

Relevance filtering, indicator decay, and hunt/detection integration converting feeds into actions.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Score sources by relevance to YOUR stack; unsubscribe from noise
2. Auto-expire indicators by type-typical lifetimes (domains days, hashes years)
3. Route intel to consumers: IOCs→matching, TTPs→hunting, actors→risk registers
4. Measure operationalized percentage — intel touched within SLA
5. Close loop: false-positive-heavy sources get demoted automatically
6. Feed confirmed hits back to sharing communities you consume from

## Common Pitfalls

- Ten thousand stale IPs blocking nothing but log space
- Intel reports read and archived without any detection change

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill detection-operations-threat-intel-operationalization
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill detection-operations-threat-intel-operationalization -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills