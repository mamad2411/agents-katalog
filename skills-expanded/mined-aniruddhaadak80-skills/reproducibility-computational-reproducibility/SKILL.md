---
name: reproducibility-computational-reproducibility
description: "Environment pinning, deterministic pipelines, and one-command reruns from raw data."
---
# Make computational results reproducible

> Environment pinning, deterministic pipelines, and one-command reruns from raw data.

**Track:** 🔬 Scientific Research · **Domain:** Reproducibility · **Level:** intermediate · **~40 min**

**Who this is for:** Researchers, PhD Students, Postdocs, Research Software Engineers

## When to Use This Skill

Environment pinning, deterministic pipelines, and one-command reruns from raw data.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Pin environments: lockfiles plus container image recorded per result
2. Version control everything including parameter files and seeds
3. Structure pipeline raw → processed → figures with explicit stages
4. Never edit intermediate files manually; regenerate instead
5. Test one-command rerun on clean machine before submission
6. Publish code/data under DOIs via archival repositories

## Common Pitfalls

- 'It works on my laptop' dependency webs
- Figures hand-tweaked after generation

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill reproducibility-computational-reproducibility
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill reproducibility-computational-reproducibility -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills