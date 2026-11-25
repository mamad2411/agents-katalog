---
name: risk-modeling-fraud-rules-vs-model
description: "Deterministic guardrails plus scored models with human review queues tuned by loss vs friction."
---
# Layer fraud rules under an ML model sensibly

> Deterministic guardrails plus scored models with human review queues tuned by loss vs friction.

**Track:** 💰 Finance & Fintech · **Domain:** Risk & Modeling · **Level:** advanced · **~40 min**

**Who this is for:** Fintech Engineers, Financial Analysts, Risk Teams, Controllers

## When to Use This Skill

Deterministic guardrails plus scored models with human review queues tuned by loss vs friction.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Start with hard rules for non-negotiables (sanctions, velocity caps)
2. Score remaining traffic with a model trained on confirmed labels only
3. Define review queue capacity; set threshold to match it, not aspiration
4. Measure false-positive friction cost alongside fraud loss prevented
5. Champion-challenger rule/model changes in shadow mode first
6. Feed analyst outcomes back into labels weekly, closing the loop

## Common Pitfalls

- Blocking based on proxy features discriminating protected groups
- Thresholds tuned once and forgotten as patterns shift

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill risk-modeling-fraud-rules-vs-model
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill risk-modeling-fraud-rules-vs-model -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills