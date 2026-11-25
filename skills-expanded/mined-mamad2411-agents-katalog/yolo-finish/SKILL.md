---
name: yolo-finish
description: Use when a feature is implemented and verified, to land it. Default path is PR + CI check, with the ship gate confirming before the irreversible merge; fast-local is the escape hatch. Includes the risk classifier whose hard triggers always stop for a human. Triggers on "ship it", "land this", "open a PR", or as the finish step of yolo-feature.
---

# yolo-finish

Land verified work. Match the rigor to the risk.

## Precondition
The branch carries `YOLO-Verified: true` (`.claude/yolo/conventions.md`). If not, run yolo-verify first.

Run finish reasoning (risk classification, summary synthesis) at the `agents.finish` tier
from `workspace/config.yaml` (inherit if unset).

## Choose the path (read `workspace/config.yaml` `finish.mode`)
- **fast-local** (`mode: local`, or user says throwaway/offline): land with a real merge
  commit — always `--no-ff` so there is a commit to carry the done-trailer (never a
  fast-forward). Normal single-checkout case:
  `git switch <base_branch> && git merge --no-ff feature/<slug> -m "yolo: merge feature/<slug>" -m "YOLO-Feature: <slug>"`.
  If `base_branch` is checked out in another worktree, run that same merge *from that
  worktree* (git refuses to update a ref checked out elsewhere — don't fight it). The
  condensed summary goes in the merge-commit message. No forge.
- **PR** (`mode: pr`, the default): push the branch and open a PR/MR
  (`gh pr create` / `glab mr create`). The PR description IS the summary — generated from
  the brief (what) + plan (how) + diff (the work) + verification (evidence) — with the
  `YOLO-Feature: <slug>` trailer kept as the body's final standalone paragraph (see *Land*).

In BOTH paths the landing MUST produce the durable done-markers (see *Land*).

## CI check (PR path; `finish.ci`)
"Has CI" means a **required check actually reports on the PR** (`gh pr checks <pr>` returns
checks / GitLab has a pipeline for the MR) — NOT merely the presence of a workflow file,
which may produce no required check.
- `auto`: if a check reports, require it green before merge; if none reports, fall back to
  the yolo-verify result as the gate.
- `require`: always demand green CI. If NO check reports, this is a hard error — surface it
  to the human (do not wait forever on a check that will never arrive).
- `off`: never wait on CI.
When polling a pending check, bound the wait (cap attempts / total time, e.g. ~20 min); on
timeout, stop and escalate to the human rather than hanging.

## Risk classifier (runs on EVERY landing — local merge and PR alike)
The hard triggers below are **path-independent**: they fire on a fast-local merge exactly as
on a PR — "just ship it locally" never skips them. Only the CI handling above is PR-specific.
Compute against the **three-dot** diff `git diff <base_branch>...feature/<slug>` (what the
branch introduced since the merge-base — two-dot `..` would fold in unrelated changes that
landed on base and falsely inflate size and sensitive-path hits) and `workspace/config.yaml` `risk.*`.

Hard triggers (always stop for the human, even when the ship gate was pre-consented, on either path):
- yolo-verify did not cleanly pass, or success_criteria were vague.
- Diff touches any `risk.sensitive_paths` glob.
- Deletes/renames a public API or widely-imported symbol.

Soft triggers (call them out at the ship gate; escalate when crossed):
- Changed lines > `risk.max_diff_lines` OR changed files > `risk.max_diff_files`.
- A new external dependency added (package-manifest change).
- New logic shipped with no accompanying tests.

## The ship gate (decides confirm vs merge)
Landing on `<base_branch>` (local merge OR PR merge) is the irreversible boundary — the
**ship gate** (`.claude/yolo/conventions.md` *The two gates*). By default it asks a human
before merging. Only two things pre-consent it: a per-feature prose "just ship it / don't
ask" from the user, or `finish.auto_merge_on_green: true` (headless/unattended runs only).
A hard trigger overrides any pre-consent, on both the local and PR paths.

Decision (the CI clause applies on the PR path; everything else applies to both paths):
- PR path with CI red/pending → never merge (red stops; pending polls, bounded as above).
- A hard trigger fired → stop, surface the specific trigger(s), wait for the human — even if pre-consented, even on the local path.
- Not pre-consented (the default) → confirm with the human before merging, even on a clean green run.
- Pre-consented AND no hard trigger AND (PR: CI green / local: yolo-verify passed) → merge; set the PR body / merge-commit summary.

Avoid the check-then-merge race: capture the reviewed head SHA at the ship gate and
merge **only that SHA** — `gh pr merge --match-head-commit <SHA>` (GitHub refuses if the
head moved; the flag is `--match-head-commit`, there is no `--sha`) — or re-confirm
CI-green + unchanged-head immediately before merging.

## Land (durable done-markers)
The landing makes the feature **done**, and that fact must survive branch deletion and
squash merges (per `.claude/yolo/conventions.md`). Produce BOTH markers:
- **The `yolo/done/<slug>` tag** — the guaranteed durable signal, independent of how the
  merge commit's message is formed: `git tag -a "yolo/done/<slug>" -m "yolo: done <slug>"`
  (push it on the PR path: `git push origin "yolo/done/<slug>"`).
- **The `YOLO-Feature: <slug>` trailer** on the landing commit. `git merge` has no
  `--trailer` flag, so put it in a trailing message paragraph:
  `git merge --no-ff feature/<slug> -m "yolo: merge feature/<slug>" -m "YOLO-Feature: <slug>"`.
  For a local squash: `git commit -m "yolo: merge feature/<slug>" --trailer "YOLO-Feature: <slug>"`
  (`git commit` *does* support `--trailer`). For a **forge** merge/squash (`gh pr merge`,
  `glab mr merge`) the commit message is composed server-side from the PR title/body — so
  put `YOLO-Feature: <slug>` as the **final paragraph of the PR body, alone on its own line
  with nothing after it**. Git parses a line as a trailer only when it sits in the message's
  last paragraph and that paragraph is all trailers — a summary section, evidence bullet, or
  any prose *after* the line silently defeats `%(trailers:key=YOLO-Feature,valueonly)`, the
  exact probe `yolo-status` runs. Because forge message composition cannot be guaranteed, on
  the PR path the **`yolo/done/<slug>` tag is the mandatory done-marker** — create and push it
  independently of the merge (above) so status stays correct even if the trailer never parses.

Without at least the tag, `yolo-status` cannot tell a shipped-and-deleted feature from one never started.

## Cleanup
After a successful merge, in this order (deleting a branch checked out in a worktree fails):
1. `git worktree remove ../.<repo-name>-worktrees/<slug>` if one was created.
2. `git branch -D feature/<slug>` (and `git push origin --delete feature/<slug>` on the PR path, if not auto-deleted by the forge).
