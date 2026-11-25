---
name: playbook-data-engineering-streaming-hardening
description: "Correct event-time semantics with bounded state and monitored watermarks."
---
# Playbook: Harden a streaming platform

> Correct event-time semantics with bounded state and monitored watermarks.

**Track:** 🗺️ Data Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~75 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Correct event-time semantics with bounded state and monitored watermarks.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Choose windowing and watermarks correctly: start with "Timestamp on event time extracted from payload, not arrival"
2. Step 2 — Make batch pipelines rerunnable by design: start with "Key every write by logical date/partition; overwrite partitions, never append blind"
3. How it fits together: Watermark lag tells the truth; dashboards lag it.

### Referenced Skills

- `streaming-modeling-stream-processing-windows`
- `pipelines-batch-pipeline-idempotency`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill streaming-modeling-stream-processing-windows && npx skills add aniruddhaadak80/skills --skill pipelines-batch-pipeline-idempotency
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills