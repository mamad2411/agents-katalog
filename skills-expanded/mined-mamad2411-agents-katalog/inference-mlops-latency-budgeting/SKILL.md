---
name: inference-mlops-latency-budgeting
description: "Allocate milliseconds across retrieval, prompting, generation, and streaming so p95 meets product targets."
---
# Budget LLM latency end to end

> Allocate milliseconds across retrieval, prompting, generation, and streaming so p95 meets product targets.

**Track:** 🤖 AI Engineering · **Domain:** Inference & MLOps · **Level:** intermediate · **~30 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Allocate milliseconds across retrieval, prompting, generation, and streaming so p95 meets product targets.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Trace one real request through every hop and record percentile timings
2. Fix a p95 target from UX research, not infrastructure convenience
3. Stream tokens to first-paint; perceived latency beats raw latency
4. Cap retrieved context by latency cost, not just token count
5. Cache stable prefixes: system prompts, few-shots, static context
6. Alert when any hop exceeds 40% of total budget for an hour

## Common Pitfalls

- Optimizing model choice while network hops dominate
- Non-streaming endpoints behind slow proxies

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill inference-mlops-latency-budgeting
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill inference-mlops-latency-budgeting -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills