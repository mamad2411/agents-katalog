---
name: playbook-data-engineering-warehouse-zero
description: "Contracted schemas, tested tables, dimensional models analysts rely on."
---
# Playbook: Warehouse from zero to trusted

> Contracted schemas, tested tables, dimensional models analysts rely on.

**Track:** 🗺️ Data Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~75 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Contracted schemas, tested tables, dimensional models analysts rely on.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Evolve schemas without breaking consumers: start with "Publish schema contracts per dataset with owner + compatibility mode (backward default)"
2. Step 2 — Apply dimensional modeling pragmatically: start with "Declare the grain of every fact table in its documentation header"
3. How it fits together: Pick the DQ variant matching your platform. Contracts precede consumers.

### Referenced Skills

- `pipelines-batch-schema-evolution-contracts`
- `streaming-modeling-dimensional-modeling-refresh`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill pipelines-batch-schema-evolution-contracts && npx skills add aniruddhaadak80/skills --skill streaming-modeling-dimensional-modeling-refresh
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills