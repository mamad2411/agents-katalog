---
name: repo-hygiene
description: >
  Repo hygiene audit and pre-commit gate for wezdeck: broken relative markdown
  links, bash -n, mermaid on staged docs, secret heuristics, line budgets,
  bilingual README.md ↔ README.zh-CN.md structural parity.
  Use when installing commit hooks, running a full-repo size/link audit, or
  when the user asks for 卫生审计 / doc-link check / line-budget review /
  README 中英文同步检查.
  Not adversarial-review and not design-review.
---

# repo-hygiene

## When

- Install or refresh the local pre-commit gate
- Full-repo hygiene report before a “全面评审” or worktree recycle
- Debug why a commit was blocked by the hygiene hook

## Do not use for

- Runtime diff quality → `adversarial-review`
- RFC / 方案 accept-reject → design-review checklist in `validation.md`

## Commands

```bash
# one-time (shared git dir → all worktrees)
skills/repo-hygiene/install-hooks.sh

# L0 (also run by the hook)
skills/repo-hygiene/run.sh pre-commit

# L1 report (summary first)
skills/repo-hygiene/run.sh audit
skills/repo-hygiene/run.sh audit --verbose
skills/repo-hygiene/run.sh audit --backticks   # opt-in path heuristic
skills/repo-hygiene/run.sh audit --strict      # fail non-allowlisted OVER-HARD

# fixtures
skills/repo-hygiene/test.sh
```

Budgets: `budgets.conf`. README en/zh tokens: `readme-parity.conf` (checker:
`lib/readme-parity.py`). Operator notes: `docs/daily-workflow.md#repo-hygiene`.

Emergency bypass only: `WEZTERM_HYGIENE_SKIP=1`. Soften heading-anchor fails: `WEZTERM_HYGIENE_SOFT_ANCHORS=1`.

When editing either root README, update the twin in the same commit — L0 compares
heading outline, relative links, fences/tables, and durable tokens.
