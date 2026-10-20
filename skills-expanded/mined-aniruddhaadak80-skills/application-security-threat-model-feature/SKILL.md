---
name: application-security-threat-model-feature
description: "STRIDE-lite walkthrough producing mitigations wired into tickets before code exists."
---
# Threat model a feature before building it

> STRIDE-lite walkthrough producing mitigations wired into tickets before code exists.

**Track:** 🔐 Cybersecurity · **Domain:** Application Security · **Level:** intermediate · **~40 min**

**Who this is for:** Security Engineers, AppSec, DevSecOps, Compliance Teams

## When to Use This Skill

STRIDE-lite walkthrough producing mitigations wired into tickets before code exists.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Diagram the feature: actors, data flows, trust boundaries, stores
2. Walk STRIDE per boundary: spoofing, tampering, repudiation, info-disclosure, DoS, elevation
3. Rank findings by likelihood × impact; top items get design changes
4. Write mitigations as acceptance criteria in implementation tickets
5. Add abuse cases to the test plan alongside functional cases
6. Revisit the model when architecture shifts, not just annually

## Common Pitfalls

- Threat models as one-time compliance theater
- Trusting internal services implicitly across boundaries

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill application-security-threat-model-feature
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill application-security-threat-model-feature -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills