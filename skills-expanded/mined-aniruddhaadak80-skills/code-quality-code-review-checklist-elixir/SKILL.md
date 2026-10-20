---
name: code-quality-code-review-checklist-elixir
description: "Review order, comment quality, and scope discipline making PRs fast and kind."
---
# Review code like a senior engineer (Elixir)

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
7. Inspect supervision trees and mailbox depths via :observer
8. Benchmark with Benchee; watch BEAM scheduler reductions

## Common Pitfalls

- Style wars the formatter should own
- LGTM rubber-stamps on 2000-line diffs

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-code-review-checklist-elixir
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill code-quality-code-review-checklist-elixir -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills