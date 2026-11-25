---
name: ml-modeling-baseline-first-modeling
description: "Ship trivial baselines (mean, logistic, linear) to price complexity honestly."
---
# Baseline before you boost

> Ship trivial baselines (mean, logistic, linear) to price complexity honestly.

**Track:** 📊 Data Science & Analytics · **Domain:** Modeling Practice · **Level:** foundation · **~25 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

Ship trivial baselines (mean, logistic, linear) to price complexity honestly.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Predict the prior/majority class; record its metric as floor
2. Fit one linear/logistic model with sane regularization
3. Add one gradient-boosted model only if it beats baseline materially
4. Compare on identical splits and preprocessing pipelines
5. Quantify lift in business terms, not just AUC deltas
6. Deploy the simplest model within epsilon of the best

## Common Pitfalls

- Deep nets on tabular data losing to logistic regression
- Metrics improving while business outcomes don't

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill ml-modeling-baseline-first-modeling
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill ml-modeling-baseline-first-modeling -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills