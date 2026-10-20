---
name: quality-informatics-cdss-alert-review
description: "Reduce alert fatigue by measuring override reasons and retiring low-value interrupts."
---
# Tune clinical decision support alerts responsibly

> Reduce alert fatigue by measuring override reasons and retiring low-value interrupts.

**Track:** 🏥 Healthcare & Clinical · **Domain:** Quality & Informatics · **Level:** advanced · **~40 min**

**Who this is for:** Nurses, Physicians, Clinical Managers, Health Informaticists

## When to Use This Skill

Reduce alert fatigue by measuring override reasons and retiring low-value interrupts.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Pull override rates and documented reasons per alert type
2. Rank alerts by override rate × potential harm if heeded
3. Retire or narrow firing conditions of alerts overridden >90% safely
4. A/B tiered severity: interruptive only where harm is real
5. Monitor post-change for missed-event signals with named owner
6. Review the whole alert panel quarterly like a formulary

## Common Pitfalls

- Adding new alerts without retiring any, ever
- Interruptive warnings for documentation minutiae

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill quality-informatics-cdss-alert-review
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill quality-informatics-cdss-alert-review -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills