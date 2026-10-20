---
name: playbook-ai-engineering-cost-rescue
description: "Reduce monthly inference spend measurably while keeping answer quality within tolerance."
---
# Playbook: Cut LLM costs without quality collapse

> Reduce monthly inference spend measurably while keeping answer quality within tolerance.

**Track:** 🗺️ AI Engineering · **Domain:** Journey Playbooks · **Level:** journey · **~95 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Reduce monthly inference spend measurably while keeping answer quality within tolerance.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Control LLM spend without killing quality: start with "Tag every request with feature and tenant for per-unit cost attribution"
2. Step 2 — Guarantee structured outputs from LLMs: start with "Provide the JSON Schema in the prompt and ask for schema-valid output only"
3. Step 3 — Budget LLM latency end to end: start with "Trace one real request through every hop and record percentile timings"
4. How it fits together: Instrument first. Every routing/caching decision needs per-unit cost visibility or you're flying blind.

### Referenced Skills

- `inference-mlops-llm-cost-controls`
- `prompt-engineering-structured-output`
- `inference-mlops-latency-budgeting`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill inference-mlops-llm-cost-controls && npx skills add aniruddhaadak80/skills --skill prompt-engineering-structured-output && npx skills add aniruddhaadak80/skills --skill inference-mlops-latency-budgeting
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills