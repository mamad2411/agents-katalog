---
name: playbook-engineering-essentials-quality-sprint
description: "Measurable code health gains: coverage gaps, hot spots, and review debt addressed."
---
# Playbook: Run a quality improvement sprint

> Measurable code health gains: coverage gaps, hot spots, and review debt addressed.

**Track:** 🗺️ Engineering Essentials · **Domain:** Journey Playbooks · **Level:** journey · **~100 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Measurable code health gains: coverage gaps, hot spots, and review debt addressed.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Review code like a senior engineer (Rust): start with "Read description and tests FIRST to learn intent"
2. Step 2 — Profile before optimizing (Java/JVM): start with "Define target metric: p95 latency? memory ceiling? throughput?"
3. Step 3 — Debug production without stopping the world (.NET): start with "Correlate user report to trace IDs through gateway → service → data layer"
4. How it fits together: Choose targets by risk × churn. One theme per sprint; quality sprints fail by diffusion.

### Referenced Skills

- `code-quality-code-review-checklist-rust`
- `code-quality-performance-profiling-java`
- `debug-craft-production-debugging-dotnet`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-code-review-checklist-rust && npx skills add aniruddhaadak80/skills --skill code-quality-performance-profiling-java && npx skills add aniruddhaadak80/skills --skill debug-craft-production-debugging-dotnet
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills