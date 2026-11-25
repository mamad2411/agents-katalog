---
name: yolo-status
description: Use when the user asks where things stand, what's in progress, or "where was I". Computes a derived view of every feature's status from git and the briefs — nothing is read from a stored status field.
---

# yolo-status

Report the state of all features by DERIVING it from git (`.claude/yolo/conventions.md`). There is no stored status field — do not look for one.

## Procedure
1. Resolve `base_branch` (`workspace/config.yaml` `project.base_branch`, else the detection
   rule in `.claude/yolo/conventions.md`). Guard every ref with `git rev-parse --verify -q`
   before using it; if `base_branch` does not resolve, report a config error and stop. If
   `workspace/config.yaml` is absent, use the config-absent fallback from conventions.
2. Enumerate live branches once — `git for-each-ref --format='%(refname:short)' refs/heads/feature/` — so a `feature/<slug>` with **no brief** is surfaced as an `untracked-branch` row, not silently dropped.
3. For each `workspace/features/*/brief.md`, take `<slug>` from the folder. A brief with front-matter `cancelled: true` is reported as **cancelled** and otherwise skipped. Else derive status exactly per `.claude/yolo/conventions.md` *Deriving status*, in order:
   - **done** — ANY of (first match wins): tag `yolo/done/<slug>` exists, OR base history carries a `YOLO-Feature: <slug>` trailer (both durable — survive branch deletion/squash), OR (branch still present) its tip carries `YOLO-Verified: true` with a committed `verification.md`. This is what makes a shipped-and-deleted branch read as **done**, not **planned**. (`git branch --merged` is intentionally not used — it false-positives an empty freshly-cut branch.)
   - **in-progress** — `feature/<slug>` exists and is not done. Completed tasks (advisory, deduped):
     `git log <base>..feature/<slug> --format='%(trailers:key=YOLO-Task,valueonly)' | sed '/^$/d' | sort -u` (count vs the task total in `plan.md` — progress only, never the done test).
   - **planned** — brief exists, no done-evidence, and `feature/<slug>` does not exist.
4. Group rows by the brief's `milestone:` value when set. For `planned`/`in-progress` rows whose brief lists `depends_on`, flag any dependency not yet `done` as `blocked-by: <slug>`.
5. Print a compact table: slug · status · tasks(done/total, for in-progress) · milestone · blocked-by. Add a one-line resume hint from the most recent in-progress branch's last commit subject (e.g. "resume with yolo-feature <slug>").

## Constraints
- Read-only. Compute, never store. This view cannot be stale because it is recomputed each call.
