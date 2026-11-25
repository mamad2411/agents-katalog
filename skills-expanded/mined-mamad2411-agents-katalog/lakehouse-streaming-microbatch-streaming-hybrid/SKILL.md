---
name: lakehouse-streaming-microbatch-streaming-hybrid
description: "Lambda-to-Kappa migrations, microbatch cadences, and consistency contracts across paths."
---
# Blend streaming and batch where each belongs

> Lambda-to-Kappa migrations, microbatch cadences, and consistency contracts across paths.

**Track:** 🛢️ Data Engineering · **Domain:** Lakehouse & Streaming · **Level:** advanced · **~45 min**

**Who this is for:** Data Engineers, Analytics Engineers, Platform Data Teams

## When to Use This Skill

Lambda-to-Kappa migrations, microbatch cadences, and consistency contracts across paths.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Audit which consumers actually need seconds-fresh vs minutes-fresh truth
2. Consolidate logic into one stream processor where latency allows (Kappa direction)
3. Keep batch for heavy history recomputes; document boundary contracts
4. Unify schemas across paths or drift WILL create divergent truths
5. Watermark strategy consistent between live and backfill processing
6. Reconciliation job compares paths continuously; alert divergence early

## Common Pitfalls

- Two codebases implementing subtly different business logic forever
- Backfills overwriting streaming results with stale semantics

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill lakehouse-streaming-microbatch-streaming-hybrid
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill lakehouse-streaming-microbatch-streaming-hybrid -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills