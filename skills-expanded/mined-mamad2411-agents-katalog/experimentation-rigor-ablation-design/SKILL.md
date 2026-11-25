---
name: experimentation-rigor-ablation-design
description: "One-factor-at-a-time with matched budgets separating real gains from tuning luck."
---
# Design ablations that isolate contributions

> One-factor-at-a-time with matched budgets separating real gains from tuning luck.

**Track:** 🧮 ML Research Engineering · **Domain:** Experimentation Rigor · **Level:** intermediate · **~35 min**

**Who this is for:** Research Engineers, ML Scientists, PhD Researchers, Applied Scientists

## When to Use This Skill

One-factor-at-a-time with matched budgets separating real gains from tuning luck.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. List claimed components; rank by novelty and implementation cost
2. Baseline run repeated with 3+ seeds establishing variance floor
3. Remove ONE component per run; keep all else byte-identical
4. Match compute budgets across arms — bigger ablation runs cheat
5. Report deltas WITH seed variance, not single-run point estimates
6. Test interactions for top-2 components before final claims

## Common Pitfalls

- Ablations run with different hyperparameter sweeps
- Seed cherry-picking turning noise into conclusions

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-rigor-ablation-design
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-rigor-ablation-design -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills