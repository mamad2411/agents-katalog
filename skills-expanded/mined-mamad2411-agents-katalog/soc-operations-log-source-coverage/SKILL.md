---
name: soc-operations-log-source-coverage
description: "Inventory what you can see versus what attacks require, closing blind spots deliberately."
---
# Map log source coverage to attack surface

> Inventory what you can see versus what attacks require, closing blind spots deliberately.

**Track:** 🛡️ Cyber Defense & SOC · **Domain:** SOC Operations · **Level:** intermediate · **~35 min**

**Who this is for:** SOC Analysts, Detection Engineers, Threat Hunters, Blue Teams

## When to Use This Skill

Inventory what you can see versus what attacks require, closing blind spots deliberately.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. List top MITRE techniques relevant to your industry threat profile
2. Map each to required telemetry source and current ingestion status
3. Score coverage: full / partial / none per technique
4. Prioritize gaps by likelihood × detection-value
5. Fund onboarding of highest-value sources with success tests
6. Re-map quarterly; infrastructure drifts silently

## Common Pitfalls

- Ingesting everything equally, cost exploding value flat
- Coverage assumed rather than tested with synthetic events

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill soc-operations-log-source-coverage
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill soc-operations-log-source-coverage -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills