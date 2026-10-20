---
name: inference-optimization-speculative-decoding-tuning
description: "Drafter selection, acceptance-rate monitoring, and batch-interaction effects in production serving."
---
# Tune speculative decoding without regressing quality

> Drafter selection, acceptance-rate monitoring, and batch-interaction effects in production serving.

**Track:** 🧮 ML Research Engineering · **Domain:** Inference Optimization · **Level:** advanced · **~45 min**

**Who this is for:** Research Engineers, ML Scientists, PhD Researchers, Applied Scientists

## When to Use This Skill

Drafter selection, acceptance-rate monitoring, and batch-interaction effects in production serving.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Match drafter to target on YOUR distribution; measure acceptance rate per task class
2. Tune speculation length by observed acceptance — longer drafts waste on rejection
3. Watch batching interaction: gains shrink as batch size fills GPUs
4. Verify output distribution equivalence against target-only sampling
5. Re-evaluate whenever either model updates; pairs drift together
6. Track tokens-per-second AND cost-per-token separately; they optimize differently

## Common Pitfalls

- Acceptance rates from benchmarks failing on domain jargon
- Quality regressions hidden inside 'equivalent' temperature settings

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill inference-optimization-speculative-decoding-tuning
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill inference-optimization-speculative-decoding-tuning -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills