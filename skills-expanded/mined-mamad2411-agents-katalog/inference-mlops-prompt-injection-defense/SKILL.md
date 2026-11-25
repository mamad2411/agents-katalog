---
name: inference-mlops-prompt-injection-defense
description: "Treat all retrieved content as untrusted input: isolate instructions from data, gate actions, and fuzz continuously."
---
# Defend pipelines against prompt injection

> Treat all retrieved content as untrusted input: isolate instructions from data, gate actions, and fuzz continuously.

**Track:** 🤖 AI Engineering · **Domain:** Inference & MLOps · **Level:** advanced · **~40 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Treat all retrieved content as untrusted input: isolate instructions from data, gate actions, and fuzz continuously.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Separate instruction and data channels structurally, not just by prose
2. Never grant the executor credentials beyond the current task's scope
3. Gate outbound actions (email, payments, deletes) behind policy checks
4. Strip or neutralize instruction-like patterns in retrieved documents
5. Maintain an injection corpus from public benchmarks plus your own red-team finds
6. Re-run the corpus in CI whenever prompts or tools change

## Common Pitfalls

- Trusting PDFs or web pages as benign context
- Human-in-the-loop rubber-stamping high-volume approvals

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill inference-mlops-prompt-injection-defense
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill inference-mlops-prompt-injection-defense -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills