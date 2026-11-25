---
name: git-submodule-history-removal
description: >-
  Composer — remove a submodule from a repository's COMPLETE history: pre-rebase
  classification of every commit that touched the path (INTRO / POINTER-UPDATE /
  MIXED), a scripted worktree-isolated rebase dropping those commits, refresh-1
  audited cleanup (worktree, backup branches, path remnant), refresh-2 baseline
  verification (zero residual classification, untouched index/untracked
  evidence), a deliberate fast-forward of the target branch, push with
  --force-with-lease, and post-push mirror/backup refresh.
category: Git & Repository Management
---

# Git Submodule History Removal (v1)

> **Name:** git-submodule-history-removal<br>
> **Description:** Composer — remove a submodule from a repository's COMPLETE
> history with pre-rebase classification, worktree-isolated scripted rebase,
> refresh-1 audited cleanup, refresh-2 baseline verification, deliberate
> fast-forward, and gated push<br>
> **Category:** Git & Repository Management

## Composition Rationale

This skill is a top-level composer. It owns only the domain-level
orchestration (target selection, gate sequencing, cleanup audit, push
authorization) and delegates determinism to three siblings:

1. [`git-submodule-history-classification`](../../repair/git-submodule-history-classification/SKILL.md) —
   discovery + classification: `scripts/list-submodules.py` (registration
   inventory) and `scripts/classify-submodule-commits.py` (INTRO /
   POINTER-UPDATE / MIXED per commit). Its post-rewrite empty result is the
   composer's verification evidence.
2. [`git-commit-edit-in-worktree`](../../../basic/edit/git-commit-edit-in-worktree/SKILL.md) —
   the isolation mechanics: baseline capture, scratch worktree, plan
   emission, scripted rebase, tree-check, `reset --soft` fast-forward, and
   cleanup gates. This composer supplies the drop SHA list and consumes the
   fast-forwarded result.
3. [`git-rebase-drop-noninteractive`](../../../basic/edit/git-rebase-drop-noninteractive/SKILL.md) —
   the todo rewrite primitive (via `write-drop-todo.py` as
   `GIT_SEQUENCE_EDITOR`), reached through the composer above.

Value-add of this composer: the eleven-gate sequencing (classification →
plan → safety → isolate → amend/recovery → tree-check → fast-forward →
push → cleanup → post-push refresh), the refresh-1 audited cleanup set
(worktree registration, backup branches, `.gitmodules` removal, path
remnant — each verified, not assumed), the refresh-2 baseline proof (the
main worktree's index/untracked/porcelain evidence is byte-identical
before and after, and the classifier reports ZERO commits), and the push
gate with `--force-with-lease` — none of which live in the bases.

Bidirectional discoverability: both bases and the isolation composer list
this skill in their `## Composition by Higher-Level Skills` tables.

## Related Skills

- [`git-submodule-removal`](../../../../git-submodule-removal/SKILL.md) —
  registration-level removal (`.gitmodules`, gitlink, working copy). When
  history removal is NOT required, that skill is the lightweight path; when
  it IS required, its final commit-stage work is the composer's counterpart
  after the rewrite (the removal commit at the current tip).
- [`git-github-auth-fallback`](../../../../git-github-auth-fallback/SKILL.md) —
  push-blocker recovery (401/403 at the push gate).
- [`git-history-refinement`](../../../../git-history-refinement/SKILL.md) —
  general history-reconstruction toolkit; this composer is its
  submodule-purge specialization.
- [`git-worktree-state-fingerprint`](../../../basic/audit/git-worktree-state-fingerprint/SKILL.md) —
  byte-level capture/compare primitive consumed by the refresh-2 baseline
  gate (Gate 8).

## Environment & Dependencies

| Requirement | Version | Notes |
| ----------- | ------- | ----- |
| Python | 3.12+ | For `scripts/plan-removal.py` — stdlib only |
| Bash | 3.2+ (macOS) | For the isolation script (via the sibling composer) |
| Git | 2.x | `worktree`, `rebase -i`, `reset --soft`, `push --force-with-lease` |

## Scripts

### `scripts/plan-removal.py` — deterministic discovery half

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--repo <path>` | no | Repo root (default `.`). |
| `--path <submodule-path>` | yes | Submodule path (e.g. `browser-use_browser-use`). |
| `--json` | no | Emit the plan as JSON. |

Pipeline: resolves and validates ALL sibling base scripts (exits `1` with
the missing path if any); runs `list-submodules.py --json` and requires the
path to be registered; runs `classify-submodule-commits.py --path <path>
--scope all --json`; builds the deduplicated drop list (INTRO + all
POINTER-UPDATE commits, order-preserving SHA dedup); emits the eleven-gate
sequence with resolved absolute command lines and per-gate expectations,
including the refresh-1 cleanup set and the refresh-2 verification command.
Gate commands embed resolved absolute paths to every base script, so the
emitted plan is copy-executable from any `cwd`.

## Protocol

> **Core constraint:** the submodule's commits are dropped from history
> INSIDE an isolated worktree; the current working tree MUST NOT be touched
> (Gates 1/8 evidence). Every destructive step has a gate AND an audited
> cleanup expectation.

1. **Prerequisite gate** — confirm the path is still registered:
   `python3 <plan-removal> --path <path> --json`. NOT-registered paths
   (already removed at registration level) route to a fresh plan with empty
   drop list — still valid if the gitlink remains in history.
2. **Classification gate** — plan-removal's output: INTRO / POINTER-UPDATE /
   MIXED counts and the deduplicated drop list. Present to the user: every
   SHA + subject that will be dropped. MIXED commits (path + other files in
   the same commit) are NOT auto-dropped: they require a per-file split
   decision (see the isolation gate below).
3. **Safety gate** — `git branch backup/removal-<path>` at current HEAD
   (also recorded by the isolation plan), plus an apply-not-pop safety stash
   per
   [`git-pre-execution-safety-stash`](../../../../git-pre-execution-safety-stash/SKILL.md)
   when the worktree carries uncommitted work.
4. **Isolate gate** — delegate to
   [`git-commit-edit-in-worktree`](../../../basic/edit/git-commit-edit-in-worktree/SKILL.md):
   its plan gate for the FIRST drop SHA (repeat per SHA), then its
   safety/isolate mechanics inside the scratch worktree. The todo scrub is
   `git-rebase-drop-noninteractive`'s `write-drop-todo.py` with the drop SHA
   list — only SHAs present in the branch being rewritten are rewritten;
   cross-branch SHAs in the list are archive-verified, never fabricated. The
   rebase's LAST todo line MUST still be a `pick` (a trailing `drop` would
   chop the branch tip) — check the generated todo by running the writer
   with `--dry-run` against a dry-run rebase todo if in doubt.
5. **Amend / interruption-recovery gate** — per the isolation composer:
   `git commit -C <sha>` recovery for interrupted strips, `GIT_EDITOR=true`
   continues after conflict resolution, and NEVER `git commit --amend`
   mid-rebase.
6. **Tree-check gate** — in the worktree: `git rev-parse HEAD^{tree}`; the
   dropped commits are gone; `git diff --stat backup/removal-<path> HEAD`
   shows ONLY path-removal deltas and the MIXED splits decided in Gate 2.
7. **Fast-forward gate** — on the MAIN worktree:
   `git reset --soft rebase-<path>`; then the refresh-2 baseline check below
   (Gate 8). The old index may show the removed submodule as a staged
   addition — that is the STOP condition signal, not a desired state: never
   commit it; resolve via a deliberate preservation branch, then re-run
   Gate 8.
8. **Refresh-2 baseline gate** — delegate capture/compare to
   [`git-worktree-state-fingerprint`](../../../basic/audit/git-worktree-state-fingerprint/SKILL.md):
   `worktree-state-fingerprint.py capture --repo <main-worktree> --out
   <scratch>/baseline-post.json`, then `compare --pre
   <scratch>/baseline-pre.json --post <scratch>/baseline-post.json`
   (byte-level hashes of porcelain, `git ls-files -s`, staged/worktree
   binary diffs, untracked listing) — must report IDENTICAL except
   documented expected deltas; also re-run
   `classify-submodule-commits.py --path <path> --scope all --json`: MUST
   print ZERO commits. Any residual classification or baseline mismatch =
   STOP, restore from `backup/removal-<path>`.
9. **Push gate** (explicit user authorization) — push the rewritten branch
   with `--force-with-lease` from the main worktree. On 401/403, invoke
   [`git-github-auth-fallback`](../../../../git-github-auth-fallback/SKILL.md)
   before retrying.
10. **Refresh-1 cleanup gate** — the audited cleanup set, each item
    verified after execution:
    - `git worktree remove <scratch> --force` and confirm the worktree list
      no longer shows it;
    - `git branch -D rebase-<path> backup/removal-<path>` (only after push
      confirmation);
    - `rm -rf <path>` remnant removal when the working dir was checkouted
      directly against an old intermediate commit;
    - `.gitmodules` section removal + `git rm --cached <path>` when the
      registration is also being retired (delegate form to
      [`git-submodule-removal`](../../../../git-submodule-removal/SKILL.md)'s
      registration protocol).
11. **Post-push gate** — refresh mirrors / backup clones that tracked the
    rewritten branch (the push-with-lease destination hosts), and re-run
    `list-submodules.py --json` to confirm the path is absent from the
    registration inventory.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| -------- | --------------------- |
| (none yet) | This skill IS the top-level composer in its domain. |

## Prohibited Behaviors

- **Dropping MIXED commits without a per-file split decision** — their
  non-submodule content is real work.
- **Running the rebase in the main worktree** — the isolation composer's
  core constraint applies.
- **Committing a resurrected staged gitlink** (Gate 7/8 mismatch) — STOP,
  restore, and deliberately migrate the worktree instead.
- **`git reset --hard`** anywhere in the rewrite.
- **Pushing without explicit user authorization** — Gate 9 is a human
  gate.
- **Deleting the backup branch BEFORE the push confirmation**.
- **Trusting empty `--porcelain` as baseline proof** — always the hashed
  index/binary/untracked evidence.

## Common Pitfalls

| Pitfall | Solution |
| ------- | -------- |
| Drop list contains SHAs not on the rewritten branch | Same SHA reached from several branches; harmless in the todo writer (no match = no rewrite); the dedup in plan-removal already collapses repeats. |
| `rebase -i` shows the submodule's INTRO line as `drop` by subject prefix too early (misplacement guard) | Verify the drop line sits directly under the `pick` of the commit whose tree the rebase is rebuilding; a wrong `pick` above it silently re-introduces the gitlink. |
| `.gitmodules` conflict mid-rebase | Resolve, `git add .gitmodules`, continue with `GIT_EDITOR=true`. |
| `fatal: '<branch>' is already used by worktree` | Fresh `--purpose` token or `git worktree prune`. |
| Push rejected despite lease | Fetch, re-run classifier to confirm re-created commits (someone pushed INTRO again while offline), decide with the user. |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
