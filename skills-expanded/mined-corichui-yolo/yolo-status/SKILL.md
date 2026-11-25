---
name: yolo-status
description: Use when the user asks where things stand, what's in progress, what's landed, or "where was I" in a YOLO repo. Derives every feature's status from git and the briefs; nothing is read from a stored status field.
---

# yolo-status

Report every feature's state by deriving it from git, exactly per
`../../yolo/conventions.md` *Deriving status*. There is no stored status. Don't look for one.

## Procedure
1. Resolve `base_branch` (config, else the detection rule). Guard refs with
   `git rev-parse --verify -q`; if base doesn't resolve, report a config error and stop.
2. Collect evidence once, not per feature:
   - subjects of merges made on base: `git log --first-parent <base> --merges --format=%s`
   - first-parent line of base: `git rev-list --first-parent <base>`
   - `YOLO-Feature` trailers on base, and `yolo/done/*` tags
   - live branches: `git for-each-ref --format='%(refname:short)' refs/heads/feature/`
3. For each `workspace/features/*/brief.md` (slug = folder name), classify in order:
   cancelled → landed → verified → in-progress → planned. Use the slug-boundary match for
   merge subjects so `csv` never matches `csv-export`.
4. Add an **untracked-branch** row for every `feature/<slug>` with no brief.
5. For `planned`/`in-progress` rows whose brief has `depends_on`, mark any dependency that
   hasn't landed as `blocked-by: <slug>`.
6. Print a compact table: slug · status · milestone · blocked-by · last commit date on the
   branch (in-progress only). Group by `milestone` when set. End with one line naming the
   most recently touched in-progress branch.

## Constraints
- Read-only. Compute, never store.
