---
name: git-checkout-branch
description: Switches to a named branch; creates a new local branch only after explicit confirmation.
disable-model-invocation: true
---

# Git checkout / switch branch

`branch` = name from this message (trimmed). If missing, ask once and stop.

## Steps

1. `git status --short`. If the working tree is dirty and `git switch` would fail, report and stop — commit/stash/discard only if the user says so in this message.
2. `git fetch --all` when network is allowed (skip and say so if forbidden).
3. Resolve and switch:
   - **Local `branch` exists** → `git switch branch`
   - **Only on remote** → `git switch branch` if Git tracks it unambiguously; else `git switch -c branch --track origin/branch`
   - **Neither local nor `origin/branch`** → authorization gate (next section)
4. **Done when:** HEAD is on `branch`, or you stopped at a hard stop / unanswered create gate.

## Authorization gate (missing branch)

1. State that neither local nor `origin/<branch>` was found.
2. Ask whether to **create** local `branch` from **current HEAD** (or from a base the user named).
3. Create only on a clear yes (`yes` / `proceed` / `create it`). Otherwise stop.
4. On confirm: `git switch -c branch` (or `git switch -c branch <base>` if they named a base).

## Guardrails

- No branch delete, force checkout of unrelated SHAs, or inventing names.
