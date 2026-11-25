---
name: pipelines-batch-schema-evolution-contracts
description: "Schema contracts, compatibility modes, and deprecation flows across pipeline boundaries."
---
# Evolve schemas without breaking consumers

> Schema contracts, compatibility modes, and deprecation flows across pipeline boundaries.

**Track:** 🛢️ Data Engineering · **Domain:** Batch Pipelines · **Level:** advanced · **~40 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Schema contracts, compatibility modes, and deprecation flows across pipeline boundaries.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Publish schema contracts per dataset with owner + compatibility mode (backward default)
2. CI-validate producer changes against registered contracts
3. Add columns nullable-first; never repurpose existing fields silently
4. Rename via add-new → dual-write → migrate → drop-old, with telemetry at each step
5. Notify consumer list (derived from query logs) before breaking changes
6. Archive old schema versions; make lineage queryable

## Common Pitfalls

- "Temporary" column reuse changing meaning mid-history
- Producers shipping struct changes on Friday evenings

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill pipelines-batch-schema-evolution-contracts
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill pipelines-batch-schema-evolution-contracts -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills