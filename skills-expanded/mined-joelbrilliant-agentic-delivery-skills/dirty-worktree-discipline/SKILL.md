---
name: dirty-worktree-discipline
description: Keeps agent work safe in messy repositories. Use when git status is dirty, unrelated files exist, generated artefacts are present, multiple agents share a repo, or you must commit only the intended slice without damaging someone else's work.
---

# Dirty Worktree Discipline

## Overview

Use this skill before editing, staging, committing, or reverting in a repository that already has unrelated changes.

A dirty worktree is not an excuse to stop. It is a reason to be precise.

## When to Use

- `git status` is not clean.
- Generated files are present.
- Multiple agents or humans are working in the same repo.
- You need to commit only your slice.
- You are tempted to run broad cleanup or reset commands.
- A deploy or review requires exact source state.

## Preflight

Capture:

```bash
git status --short --branch
git rev-parse --show-toplevel
git diff --name-only
git diff --cached --name-only
```

Classify files:

- yours;
- pre-existing unrelated;
- generated artefacts;
- unknown and risky;
- ignored/cache/temp.

## Rules

1. **Never run broad reset/clean by default.** No `git reset --hard`, no `git clean -fd`, no mass restore without explicit scope.
2. **Stage by path.** Use `git add path1 path2`, not `git add .`.
3. **Inspect staged diff.** Run `git diff --cached --stat` and `git diff --cached --name-only` before commit.
4. **Preserve unrelated work.** Do not format, revert, or move files outside your slice.
5. **Generated artefacts need intent.** If build output is required for deploy, say so. Otherwise leave it uncommitted.
6. **Dirty state is part of evidence.** Report what remains dirty and why.

## Commit Protocol

Before commit:

```text
Intended files:
Staged files:
Excluded dirty files:
Validation run:
```

After commit:

```text
Commit SHA:
Files committed:
Repo still dirty: yes/no
Unrelated dirty state preserved:
```

## Safe Commands

Good:

```bash
git add specific/file another/file
git diff --cached --name-only
git restore -- specific/generated-file
```

Risky, use only with explicit approval:

```bash
git add .
git reset --hard
git clean -fd
git checkout .
```

## Anti-patterns

- "Workspace was messy so I committed everything."
- "I cleaned generated files and accidentally deleted someone else's artefacts."
- "I deployed from a dirty tree but did not report it."
- "I used broad restore because the diff was noisy."
