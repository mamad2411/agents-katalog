---
name: git-under-contention
description: "Operate Git safely when multiple humans or coding agents may share a repository, checkout, index, branches, or worktrees. Use before staging, committing, pushing, merging, rebasing, creating or removing worktrees, recovering apparently lost edits, handling staged files you did not touch, or preserving unfinished agent work under parallel-session contention."
metadata:
  version: 0.2.0
---

# Git Under Contention

Preserve every participant's work when repository state may change concurrently.

## Core rule

Treat shared checkout as contested state. Stage exact paths, commit only owned changes, and leave unfamiliar hunks untouched.

## Preflight

Run bundled detector before first commit in shared checkout:

```bash
python <skill-dir>/scripts/contention_preflight.py
python <skill-dir>/scripts/contention_preflight.py --mine path/owned-by-task
```

Signals include registered worktrees, recent HEAD movement, pre-staged files, and dirty paths outside owned pathspecs. `CONTENTION` is not automatic failure – it means use isolated worktree or stricter path ownership.

Skip detector only inside isolated worktree created for current task and still run normal status checks.

## Shared-checkout rules

- Inspect `git status --porcelain`, current branch, top-level path, and staged diff before mutation.
- Stage with `git add <path>...`; avoid `git add .`, `git add -A`, and `git commit -a`.
- Review `git diff --cached --name-only` and `git diff --cached` before commit.
- Commit with explicit pathspec when repository conventions allow it.
- Leave changes outside owned paths unchanged, staged or unstaged.
- Avoid stash in contested checkout because stash captures shared state. Use task worktree or WIP commit on owned branch.
- Fetch before deciding branch freshness; do not reset shared checkout to match remote.
- Push durable work promptly so recovery does not depend on one disk.

## Worktree lifecycle

Prefer worktree per task when work is multi-file, long-running, risky, or parallel.

1. Fetch remote and create short-lived branch from intended base.
2. Create worktree at explicit validated path.
3. Record absolute root, branch, and base commit in handoff.
4. Edit, stage exact paths, commit, and push as one durable sequence.
5. Recheck dirty state and unpushed commits before cleanup.
6. Remove worktree only through repository helper when one exists.

Before recursive worktree cleanup, inspect symlinks, junctions, mounts, and dependency links. Remove links safely before recursive deletion so cleanup cannot traverse into another checkout.

## When state moves unexpectedly

- File disappears: verify `git rev-parse --show-toplevel`, branch, and HEAD before recreating it.
- HEAD changes during read-only audit: re-anchor findings to new HEAD.
- Staged files appear: inspect and preserve; do not unstage unless ownership is known.
- Push rejected as behind remote: fetch, inspect divergence, and integrate only owned branch.
- Worktree vanishes: recover from pushed branch or commits; do not guess from stale local paths.
- Generated file conflicts: regenerate once at repository-defined integration point instead of hand-merging machine output.

## Safe handoff

Report:

```text
Repo root: <absolute path>
Branch: <name>
Base: <sha>
Pushed tip: <sha or not pushed>
Owned paths: <list>
Dirty paths remaining: <list>
Other work preserved: <summary>
Next command: <single concrete action>
```

## Checklist before push

- [ ] Current root, branch, and HEAD confirmed.
- [ ] Staged paths belong only to current task.
- [ ] Cached diff reviewed.
- [ ] Unfamiliar working-tree changes preserved.
- [ ] Generated artifacts handled at canonical integration point.
- [ ] Branch pushed and remote tip confirmed.
- [ ] Cleanup skipped until worktree is clean and durable.

## Stop conditions

- Destructive reset, force-push, branch deletion, or worktree deletion could affect unowned state.
- Required file contains fresh hunks from another active task and safe merge cannot be proven.
- Target path for recursive cleanup contains unresolved links, junctions, mounts, or escapes intended workspace.

Ask owner for coordination rather than racing these conditions.

## Bundled resource

`scripts/contention_preflight.py` provides deterministic `CLEAR` or `CONTENTION` verdict, JSON output, and hermetic `--selftest`.

## Related skills

- `session-close` makes work durable before session ends.
- `verify-honestly` prevents false claims about pushed or merged state.
