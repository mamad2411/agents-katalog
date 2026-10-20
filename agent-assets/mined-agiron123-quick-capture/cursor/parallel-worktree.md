---
description: Linked git worktree detected — use worktree Docker commands and bootstrap when needed
alwaysApply: true
---

# Parallel worktree (Quick Capture)

Detect a **linked worktree**: `.git` is a **file** (not a directory).

## If `.env.worktree` is missing

Run bootstrap **before** any Docker dev command:

```bash
npm run worktree:bootstrap
```

Requires root `.env` with shared API keys. Creates Neon branch, `.env.worktree`, port block, and migrations.

## Docker commands in linked worktrees

| Use | Not |
| --- | --- |
| `npm run docker:dev:worktree` | `npm run docker:dev` |
| `npm run docker:down:worktree` | `npm run docker:down` |

## Create a new worktree (from main checkout)

```bash
npm run worktree:create -- ../quick-capture-<slug> -b feat/my-feature
cd ../quick-capture-<slug>
npm run docker:dev:worktree
```

## Reference

- Skill: `.cursor/skills/quick-capture-worktree/SKILL.md`
- Spec: `docs/features/worktree-dev.md`
