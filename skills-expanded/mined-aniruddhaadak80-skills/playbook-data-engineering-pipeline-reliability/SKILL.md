---
name: playbook-data-engineering-pipeline-reliability
description: "Rerunnable stages, freshness SLAs, and alert fatigue eliminated."
---
# Playbook: Make pipelines boring again

> Rerunnable stages, freshness SLAs, and alert fatigue eliminated.

**Track:** 🗺️ Data Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~35 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Rerunnable stages, freshness SLAs, and alert fatigue eliminated.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Make batch pipelines rerunnable by design: start with "Key every write by logical date/partition; overwrite partitions, never append blind"
2. How it fits together: Idempotency converts failures from incidents into retries.

### Referenced Skills

- `pipelines-batch-pipeline-idempotency`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill pipelines-batch-pipeline-idempotency
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills