---
name: evaluation-integrity-benchmark-selection-honesty
description: "Benchmark suites matched to target capabilities with contamination checks and honest scopes."
---
# Choose benchmarks that mean something

> Benchmark suites matched to target capabilities with contamination checks and honest scopes.

**Track:** 🧮 ML Research Engineering · **Domain:** Evaluation Integrity · **Level:** intermediate · **~30 min**

**Who this is for:** Research Engineers, ML Scientists, PhD Researchers, Applied Scientists

## When to Use This Skill

Benchmark suites matched to target capabilities with contamination checks and honest scopes.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define capability claims first; benchmarks follow claims, not reverse
2. Check train/test contamination against your corpora before trusting numbers
3. Prefer held-out private sets for anything heading to publication
4. Report full suite including unfavorable tasks, not highlights
5. State statistical significance; differences inside noise bands are ties
6. Archive exact eval configs alongside results permanently

## Common Pitfalls

- SOTA claimed on benchmarks the model effectively memorized
- Task suites drifting between model generations

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill evaluation-integrity-benchmark-selection-honesty
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill evaluation-integrity-benchmark-selection-honesty -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills