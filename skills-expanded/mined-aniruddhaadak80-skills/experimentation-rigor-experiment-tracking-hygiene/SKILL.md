---
name: experimentation-rigor-experiment-tracking-hygiene
description: "Every run reproducible from logged config + code version + data snapshot reference."
---
# Keep experiment tracking trustworthy

> Every run reproducible from logged config + code version + data snapshot reference.

**Track:** 🧮 ML Research Engineering · **Domain:** Experimentation Rigor · **Level:** foundation · **~30 min**

**Who this is for:** Research Engineers, ML Scientists, PhD Researchers, Applied Scientists

## When to Use This Skill

Every run reproducible from logged config + code version + data snapshot reference.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Log config automatically from source of truth, never hand-transcribed
2. Attach git SHA + diff for uncommitted changes to every run
3. Reference datasets by content hash or immutable version tag
4. Name runs by hypothesis ID, not creative adjectives
5. Tag runs: baseline / candidate / aborted / champion with promotion reasons
6. Weekly review: kill zombie experiments, archive stale branches

## Common Pitfalls

- Best result ever that nobody can rerun
- Config drift between what ran and what was documented

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-rigor-experiment-tracking-hygiene
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill experimentation-rigor-experiment-tracking-hygiene -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills