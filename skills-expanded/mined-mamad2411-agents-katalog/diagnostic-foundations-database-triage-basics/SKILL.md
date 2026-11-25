---
name: diagnostic-foundations-database-triage-basics
description: "Structured first-response: load vs lock vs query-plan diagnosis under pressure."
---
# Triage 'the database is slow' alarms

> Structured first-response: load vs lock vs query-plan diagnosis under pressure.

**Track:** 🧰 Engineering Essentials · **Domain:** Diagnostic Foundations · **Level:** intermediate · **~30 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Structured first-response: load vs lock vs query-plan diagnosis under pressure.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Classify first: connection exhaustion, lock waits, CPU, IO wait, or single bad query
2. Check active queries ordered by duration; kill nothing without recording its text
3. Compare current plan vs known-good for suspect queries
4. Correlate deploys/migrations/batch jobs against symptom onset time
5. Mitigate (timeout, queue depth, read replica shift) before root-causing fully
6. Write the incident note while terminal history still exists

## Common Pitfalls

- Restarting the primary destroying diagnostic evidence
- Adding indexes during incident without load testing

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill diagnostic-foundations-database-triage-basics
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill diagnostic-foundations-database-triage-basics -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills