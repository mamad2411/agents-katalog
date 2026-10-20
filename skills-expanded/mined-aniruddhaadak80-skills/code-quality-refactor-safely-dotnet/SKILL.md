---
name: code-quality-refactor-safely-dotnet
description: "Characterization tests, small mechanical steps, and clean-cut commits keeping refactors boring."
---
# Refactor without breaking behavior (.NET)

> Characterization tests, small mechanical steps, and clean-cut commits keeping refactors boring.

**Track:** 🧰 Engineering Essentials · **Domain:** Code Quality · **Level:** intermediate · **~35 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Characterization tests, small mechanical steps, and clean-cut commits keeping refactors boring.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Pin current behavior with characterization tests where gaps exist
2. Plan steps each leaving tests green; commit per step
3. Prefer mechanical moves (extract, inline, rename) over clever rewrites
4. Keep behavior changes in separate PRs from structure moves
5. Measure complexity delta honestly; stop when readability peaks
6. Leave the campsite cleaner but don't rebuild the forest
7. Review GC modes per workload type (workstation/server)
8. Benchmark with BenchmarkDotNet; beware allocation in loops

## Common Pitfalls

- Big-bang rewrites losing hidden behaviors
- 'While I'm here' feature creep inside refactor PRs

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-refactor-safely-dotnet
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-refactor-safely-dotnet -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills