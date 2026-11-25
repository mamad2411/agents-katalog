---
name: inference-mlops-llm-cost-controls
description: "Route by task complexity, cache aggressively, and enforce budgets so unit economics hold as usage grows."
---
# Control LLM spend without killing quality

> Route by task complexity, cache aggressively, and enforce budgets so unit economics hold as usage grows.

**Track:** 🤖 AI Engineering · **Domain:** Inference & MLOps · **Level:** intermediate · **~30 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Route by task complexity, cache aggressively, and enforce budgets so unit economics hold as usage grows.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Tag every request with feature and tenant for per-unit cost attribution
2. Route simple tasks to small models using a trained classifier or heuristics
3. Cache exact and semantic matches; measure hit-rate weekly
4. Compress context: prune, summarize history, cap tool outputs
5. Set per-key and per-tenant daily caps with graceful degradation paths
6. Review the top ten most expensive prompts monthly and shrink them

## Common Pitfalls

- Premium model answering 'is this email spam?'
- Semantic caches keyed too loosely, returning stale answers

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill inference-mlops-llm-cost-controls
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill inference-mlops-llm-cost-controls -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills