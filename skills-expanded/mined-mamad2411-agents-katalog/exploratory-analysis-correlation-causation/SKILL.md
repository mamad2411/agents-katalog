---
name: exploratory-analysis-correlation-causation
description: "Stress-test relationships with confounder thinking and simple falsification checks."
---
# Avoid correlation traps in stakeholder analyses

> Stress-test relationships with confounder thinking and simple falsification checks.

**Track:** 📊 Data Science & Analytics · **Domain:** Exploratory Analysis · **Level:** intermediate · **~25 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

Stress-test relationships with confounder thinking and simple falsification checks.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Ask what could drive both variables; list top three confounders
2. Stratify or control for obvious confounders and see if effect survives
3. Run falsification tests: effect should vanish under placebo splits
4. Frame findings as associations unless design supports causality
5. Pre-register hypotheses for decisions that matter
6. Communicate uncertainty ranges, never naked point estimates

## Common Pitfalls

- Simpson's paradox flipping conclusions after segmentation
- Post-hoc story fitting presented as discovery

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill exploratory-analysis-correlation-causation
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill exploratory-analysis-correlation-causation -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills