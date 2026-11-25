---
name: code-quality-code-review-checklist-dotnet
description: "Review order, comment quality, and scope discipline making PRs fast and kind."
---
# Review code like a senior engineer (.NET)

> Review order, comment quality, and scope discipline making PRs fast and kind.

**Track:** 🧰 Engineering Essentials · **Domain:** Code Quality · **Level:** foundation · **~25 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Review order, comment quality, and scope discipline making PRs fast and kind.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Read description and tests FIRST to learn intent
2. Check correctness and security before style nits
3. Comment questions/observations vs required-changes distinctly
4. Keep nitpicks batched as one optional pass
5. Approve explicitly when remaining items are optional
6. Aim same-day first response; latency kills momentum
7. Review GC modes per workload type (workstation/server)
8. Benchmark with BenchmarkDotNet; beware allocation in loops

## Common Pitfalls

- Style wars the formatter should own
- LGTM rubber-stamps on 2000-line diffs

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-code-review-checklist-dotnet
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-code-review-checklist-dotnet -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills