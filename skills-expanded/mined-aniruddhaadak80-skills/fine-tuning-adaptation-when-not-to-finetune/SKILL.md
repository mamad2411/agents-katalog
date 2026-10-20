---
name: fine-tuning-adaptation-when-not-to-finetune
description: "Pick the cheapest adaptation layer that solves the problem using a decision ladder."
---
# Decide between prompting, RAG, and fine-tuning

> Pick the cheapest adaptation layer that solves the problem using a decision ladder.

**Track:** 🤖 AI Engineering · **Domain:** Fine-tuning & Adaptation · **Level:** foundation · **~20 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Pick the cheapest adaptation layer that solves the problem using a decision ladder.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Try prompt engineering first: most 'model gaps' are specification gaps
2. If failures are missing knowledge, add retrieval, not weights
3. If failures are format/tone/style consistency, consider light fine-tuning
4. Estimate 12-month cost per option including maintenance, not just training
5. Prototype the winner in one week; if gains are marginal, revert to cheaper tier
6. Document the decision and revisit when base models jump a generation

## Common Pitfalls

- Fine-tuning to inject facts that go stale within months
- Skipping the cheap baseline entirely

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill fine-tuning-adaptation-when-not-to-finetune
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill fine-tuning-adaptation-when-not-to-finetune -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills