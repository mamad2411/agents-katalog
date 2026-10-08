---
name: cid-publish
description: >-
  Performs controlled Git publication for CID (explicit staging, one commit,
  optional tag, push main). Use when explicitly invoked as cid-publish, or when
  the user authorizes a controlled commit/tag/push and forbids broad staging.
disable-model-invocation: true
---

# cid-publish

SOLO publicación Git controlada. `AGENTS.md` is authority. Do not edit source to “fix” publish blockers unless the task explicitly allows.

## Preconditions

1. `cd /opt/SERVICIOS_CINE && source .venv/bin/activate`
2. Confirm branch, HEAD, `origin/main`, ahead/behind, and worktree:
   - `git branch --show-current`
   - `git rev-parse HEAD`
   - `git rev-parse origin/main`
   - `git rev-list --left-right --count origin/main...main`
   - `git status --short`
3. Repo must be clean except authorized paths. Any unexpected delta → STOP.
4. Run `git diff --check` (and staged check after staging).

## Staging

- Stage only authorized paths with explicit `git add -- <path>…`
- NEVER `git add .` / `git add -A` / `git add --all`

### Explicitly forbidden Git operations

- `git add .`
- `git add -A`
- `git add --all`
- `git push --force`
- `git push -f`
- `git reset --hard`
- force push (any form)
- automatic reset
- automatic rebase
- automatic merge
- `--amend` unless explicitly authorized

- Verify:
  - `git diff --cached --name-only`
  - `git diff --cached --check`
  - `git diff --cached --stat`
- Staged set must equal authorized publish set exactly. Else STOP.

## Commit

- Create exactly one commit with the task-specified message (HEREDOC).
- No `--amend`. No `--no-verify` unless explicitly authorized.
- Verify parent SHA and that the commit contains only authorized paths.
- Require clean worktree/index after commit (unless task allows leftover untracked).

## Remote / push

1. `git fetch origin main`
2. If `origin/main` moved unexpectedly vs expected baseline → STOP. No pull/rebase/merge/reset.
3. `git push origin main` (no force).
4. Re-fetch and verify `HEAD == origin/main`, ahead/behind `0 0`, clean status.
5. Create/push tag **only** when the task explicitly requires it; never invent tags.

## Delivery

Return:

```text
PUBLISH_APPROVED=True/False
BASELINE_SHA=
NEW_COMMIT_SHA=
PARENT_SHA=
COMMIT_PATHS=
MAIN_PUSH_SUCCEEDED=True/False
TAG_CREATED=True/False
REMOTE_MAIN_SHA=
FINAL_AHEAD_BEHIND=
REPOSITORY_CLEAN=True/False
```

STOP on any discrepancy. No automatic recovery via rebase/merge/reset.
