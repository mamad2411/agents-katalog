---
name: ml-modeling-leakage-prevention
description: "Split-aware preprocessing, temporal boundaries, and feature provenance keeping offline gains real online."
---
# Prevent data leakage in ML pipelines

> Split-aware preprocessing, temporal boundaries, and feature provenance keeping offline gains real online.

**Track:** 📊 Data Science & Analytics · **Domain:** Modeling Practice · **Level:** advanced · **~35 min**

**Who this is for:** Data Scientists, Analysts, Research Scientists, Product Analysts

## When to Use This Skill

Split-aware preprocessing, temporal boundaries, and feature provenance keeping offline gains real online.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Split temporally when production predicts the future
2. Fit scalers/imputers/encoders inside folds only, never full data
3. Ban features unavailable at prediction timestamp (audit with data team)
4. Group correlated rows (same user/device) into same split side
5. Track feature computation code versions with model artifacts
6. Validate: offline-vs-online correlation checked each release

## Common Pitfalls

- Random shuffles leaking user histories across train/test
- Target encoding fit on full dataset

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill ml-modeling-leakage-prevention
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill ml-modeling-leakage-prevention -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills