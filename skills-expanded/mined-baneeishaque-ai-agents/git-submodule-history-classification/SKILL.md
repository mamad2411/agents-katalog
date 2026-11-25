---
name: git-submodule-history-classification
description: >-
  Base primitive for the submodule-history-removal workflow: list every
  submodule in a parent repo WITH ITS REMOTE (name/path/url/status), and
  classify every commit that touched a submodule path (INTRO /
  POINTER-UPDATE / MIXED / REMOVAL) with per-commit evidence. Branch-scope
  exclusion (checkpoint branches). JSONL output consumed by
  git-submodule-history-removal and git-commit-edit-in-worktree.
category: Git & Repository Management
---

# Git Submodule History Classification (v1)

> **Name:** git-submodule-history-classification<br>
> **Description:** Base primitive — submodule inventory with remotes and
> per-commit history classification (INTRO / POINTER-UPDATE / MIXED / REMOVAL)<br>
> **Category:** Git & Repository Management

## Composition Rationale

This skill is a base primitive: both the inventory-with-remotes listing and
the commit classification are deterministic read-only discovery steps reused
by every composer that plans submodule history surgery. Inlining them would
split the SSOT and force re-derivation. Known composers:

- [`git-commit-edit-in-worktree`](../../../basic/edit/git-commit-edit-in-worktree/SKILL.md) —
  shells out to `scripts/classify-submodule-commits.py` for the scoping half
  of its plan step.
- [`git-submodule-history-removal`](../../lifecycle/git-submodule-history-removal/SKILL.md) —
  shells out to both scripts for its Inventory + Discovery gate.

## Related Skills

- [`git-submodule-uninitialized-audit`](../../../../git-submodule-uninitialized-audit/SKILL.md) —
  full recursive reachability audit (top-level + nested + orphan); this skill
  is the lean inventory + history classification counterpart.
- [`git-submodule-dead-upstream-audit`](../../../../git-submodule-dead-upstream-audit/SKILL.md) —
  upstream reachability diagnosis once classification marks a submodule for
  removal.
- [`git-commit-details-audit`](../../../../git-commit-details-audit/SKILL.md) —
  high-fidelity per-commit metadata when a classified commit needs deep
  inspection.

## Environment & Dependencies

| Requirement | Version | Notes |
| ----------- | ------- | ----- |
| Python | 3.12+ | Stdlib only — no pip dependencies |
| Git | 2.x | `submodule status`, `ls-files --stage`, `config -f .gitmodules`, `log/show` |

## Script A: `scripts/list-submodules.py`

Inventory with remotes — replicates the `docs/uninitialized-submodules.md`
workflow (`git submodule status` + `git config -f .gitmodules`).

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--repo <path>` | no | Repo root (default: current working directory). |
| `--uninitialized-only` | no | Only output `uninitialized` submodules. |
| `--json` | no | JSONL (default: TSV `name<TAB>path<TAB>url<TAB>status`). |
| `--report <path>` | no | Write a markdown table report to PATH instead of stdout. |

**Behavior:**

1. `git -C <repo> ls-files --stage` — gitlink entries (mode `160000`) give
   the exact submodule path and recorded SHA.
2. `git config -f .gitmodules --get-regexp '^submodule\..*\.path$'` — resolve
   name → path; per name, `--get submodule.<name>.url` for the remote.
3. `git -C <repo> submodule status` — status flag per path; mapped to
   `initialized` / `uninitialized` / `plus` / `conflict`.
4. `--report` emits the markdown table `| Submodule | Path | Remote URL |`
   sorted by path (the `docs/uninitialized-submodules.md` convention).

**Guardrails:** read-only; `GIT_PAGER=cat` on every git invocation; the
report is written ONLY to the path explicitly passed via `--report` — the
skill never auto-creates docs.

## Script B: `scripts/classify-submodule-commits.py`

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--repo <path>` | no | Repo root (default `.`). |
| `--path <submodule-path>` | yes | Submodule path relative to root (e.g. `anthropics_skills`). |
| `--scope <commit\|all>` | no | `all` (default) = all branches; `commit` = only branches whose `--contains` the `--contains` SHA. |
| `--contains <sha>` | no | Candidate SHA for `--scope commit`. |
| `--exclude-branches <glob>` | no | Repeatable; default `entire/*`, `backup/*`, `backup2/*` (checkpoint branches). |
| `--first-parent` | no | Restrict to first-parent history. |
| `--json` | no | JSONL `{sha, branch, subject, class, files}` (default: human table). |

**Behavior:**

1. **Branch enumeration with skip** — `git branch -a` filtered through the
   `--exclude-branches` globs (matched against both the local name and the
   `remotes/`-stripped name).
2. For each surviving branch: `git log <branch> --format=%H\|%s -- <path>`.
3. Per SHA: `git show --format= --raw <sha> -- <path>` for the mode delta,
   plus `git show --format= --name-only <sha>` for the full file list.
4. **Classification** — `INTRO` (mode `000000` → `160000`, i.e. the gitlink
   is added); `REMOVAL` (mode `160000` → `000000`, the entry is deleted);
   `POINTER-UPDATE` (only the gitlink SHA changed, no other files);
   `MIXED` (touches the path AND other files — surfaced with the file list).
5. Exit codes: `0` ok; `2` path never existed in any scanned branch (empty
   result for `--scope all`); `3` usage error.

**Guardrails:** read-only; `GIT_PAGER=cat`; the default branch exclusion list
is explicit and documented; `--exclude-branches` is repeatable.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| -------- | --------------------- |
| [`git-commit-edit-in-worktree`](../../../basic/edit/git-commit-edit-in-worktree/SKILL.md) | Calls `scripts/classify-submodule-commits.py --repo <repo> --path <path> --scope all --json` in its plan step to locate the INTRO commit and compute the rebase base `<intro>^`. |
| [`git-submodule-history-removal`](../../lifecycle/git-submodule-history-removal/SKILL.md) | Calls `scripts/list-submodules.py --repo <repo> --json` and `scripts/classify-submodule-commits.py --repo <repo> --path <path> --scope all --json` at its Inventory + Discovery gate; consumes the JSONL classification to build the drop list and the post-rewrite zero-commits verification. |

## Prohibited Behaviors

- **Mutating anything** — both scripts are read-only discovery; any plan
  stage that mutates history belongs to the composers.
- **Auto-writing `docs/uninitialized-submodules.md`** — the report is written
  only to the path passed via `--report`.
- **Scanning checkpoint branches without an explicit override** — the
  `entire/*` / `backup/*` / `backup2/*` default skip list keeps rewrite
  planning scoped to live history.

## Common Pitfalls

| Pitfall | Solution |
| ------- | -------- |
| Classification runs over dozens of checkpoint branches | Default `--exclude-branches` already skips them; add more via the repeatable flag. |
| Root commit introduces the submodule | `git show --raw` against the empty tree yields mode `000000` → `160000`; classified as INTRO correctly. |
| A path appears on branches with divergent history | Output is per `(sha, branch)`; dedupe on `sha` at the composer level when only history presence matters. |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
