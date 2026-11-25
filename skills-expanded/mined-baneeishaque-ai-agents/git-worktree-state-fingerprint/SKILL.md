---
name: git-worktree-state-fingerprint
description: >-
  Base primitive — capture and compare a byte-level fingerprint of a Git
  worktree's state (porcelain, index, staged diff, worktree diff, untracked
  set, HEAD, commit count) for pre/post history-rewrite and safety
  verification.
category: Git & Repository Management
---

# Git Worktree State Fingerprint (v1)

> **Name:** git-worktree-state-fingerprint<br>
> **Description:** Base primitive — byte-level worktree state capture + delta comparison<br>
> **Category:** Git & Repository Management

## Composition Rationale

This skill is a base primitive: the capture/compare mechanics are
deterministic and were previously re-derived ad hoc — as a prose pipeline in
the composer `git-commit-edit-in-worktree` (Gates 1 and 8) and hand-rolled a
second time in `git-submodule-history-removal`'s refresh-2 baseline gate.
Extraction centralizes the hash contract (raw stdout bytes of four git
commands) in one script. Known composers/consumers:

- [`git-commit-edit-in-worktree`](../../edit/git-commit-edit-in-worktree/SKILL.md)
  — Gates 1 and 8: captures the pre-rewrite fingerprint, then compares the
  post-rewrite fingerprint and requires byte-identical state except the
  documented expected deltas.
- [`git-submodule-history-removal`](../../../submodule/lifecycle/git-submodule-history-removal/SKILL.md)
  — its refresh-2 baseline verification gate delegates capture/compare to
  this script.

## Related Skills

- [`git-pre-execution-safety-stash`](../../../../git-pre-execution-safety-stash/SKILL.md)
  — stash-based, recoverable safety snapshot; this skill is read-only
  verification evidence, NOT a backup.
- [`git-commit-replace-and-replay`](../../edit/git-commit-replace-and-replay/SKILL.md)
  — the in-place replacement primitive whose post-replay verification pairs
  with this fingerprint.

## Environment & Dependencies

| Requirement | Version | Notes |
| ----------- | ------- | ----- |
| Python | 3.12+ | Stdlib only — no pip dependencies |
| Git | 2.x | All commands run via `git -C <repo>` |

## CLI Contract

[`scripts/worktree-state-fingerprint.py`](scripts/worktree-state-fingerprint.py):

| Subcommand | Arguments | Description |
| ---------- | --------- | ----------- |
| `capture` | `--repo <path> --out <snapshot.json>` | Writes the fingerprint snapshot; prints the repo and short HEAD. |
| `compare` | `--pre <a.json> --post <b.json> [--json]` | Reports every field delta; exit 1 when any delta exists. |

**Fingerprint fields:**

| Field | Source | Stored as |
| ----- | ------ | --------- |
| `porcelain` | `git status --porcelain` | raw text |
| `hashes.index` | `git ls-files -s` | sha256 of raw stdout bytes |
| `hashes.staged_diff` | `git diff --cached --binary` | sha256 |
| `hashes.worktree_diff` | `git diff --binary` | sha256 |
| `hashes.untracked` | `git ls-files --others --exclude-standard` | sha256 |
| `head` | `git rev-parse HEAD` | full SHA |
| `commit_count` | `git rev-list --count HEAD` | integer |

**Hash parity:** the four hashes are byte-for-byte compatible with the shell
pipeline `git <cmd> | shasum -a 256` (hash of the command's stdout bytes,
including the trailing newline).

**Exit codes:** `0` capture ok / compare identical; `1` compare found
deltas; `2` usage, I/O, or git error.

## Protocol

1. **Capture pre** — before the operation under verification:

   ```bash
   python3 .agents/skills/git/basic/audit/git-worktree-state-fingerprint/scripts/worktree-state-fingerprint.py \
     capture --repo <worktree> --out <scratch>/fingerprint-pre.json
   ```

2. **Perform the operation** (history rewrite, stash lifecycle step, …).
3. **Capture post** — same command with `--out <scratch>/fingerprint-post.json`.
4. **Compare** — `compare --pre … --post …`; every reported delta must be
   individually explained against the operation's expected effects, or the
   operation STOPS. The script itself applies no tolerances.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| -------- | --------------------- |
| [`git-commit-edit-in-worktree`](../../edit/git-commit-edit-in-worktree/SKILL.md) | Gate 1 runs `capture` on the target worktree before any mutation; Gate 8 re-runs `capture` and then `compare --pre --post`, consuming the delta list to gate the edit (expected: worktree bytes identical + HEAD at the expected new tip). |
| [`git-submodule-history-removal`](../../../submodule/lifecycle/git-submodule-history-removal/SKILL.md) | Refresh-2 baseline verification runs `capture`/`compare` around the history-removal rebase instead of the previously hand-rolled shell pipeline. |

## Prohibited Behaviors

- **Applying expected-delta tolerances inside the script** — `compare`
  reports ALL deltas; deciding which deltas are acceptable is the consuming
  skill's prose contract.
- **Using this skill as a backup/restore mechanism** — it is read-only
  evidence; for recoverable snapshots use
  [`git-pre-execution-safety-stash`](../../../../git-pre-execution-safety-stash/SKILL.md).
- **Hand-editing snapshot JSON** — the hash fields are the contract.

## Common Pitfalls

| Pitfall | Solution |
| ------- | -------- |
| Comparing snapshots from two different worktrees | `repo` is recorded in each snapshot — verify both `repo` fields match before trusting a comparison. |
| Hash mismatch vs an older shell pipeline run | The pipeline must hash stdout BYTES; text-mode processing (e.g. `git status` colorized, pager active) changes bytes — the script always sets `GIT_PAGER=cat` and captures raw stdout. |
| Interpreting a `hashes.index` delta on gitlink repos | Submodule gitlink index entries can refresh during rewrite/autostash cycles — report and explain the delta; never silently accept it. |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
