---
name: git-commit-edit-in-worktree
description: >-
  Composer — edit ANY commit (drop, amend, reword, edit) without touching
  the current working tree. Mode A: scratch-worktree isolation with a
  scripted rebase todo (GIT_SEQUENCE_EDITOR), diff-tree parity vs the backup
  branch, and a reset --soft fast-forward. Mode B: dedicated-worktree
  in-place replacement delegating to git-commit-replace-and-replay, proven
  by fingerprint gates and range-diff parity.
category: Git & Repository Management
---

# Git Commit Edit In Worktree (v2)

> **Name:** git-commit-edit-in-worktree<br>
> **Description:** Composer — edit any commit (drop / amend / reword / edit)
> in an isolated `git worktree`, never touching the current working tree<br>
> **Category:** Git & Repository Management

## Composition Rationale

This skill is a composer. It does NOT re-implement the rebase-todo rewrite,
submodule commit discovery, byte-level state capture, or the in-place
replacement mechanics. It orchestrates four base skills:

1. [`git-rebase-drop-noninteractive`](../git-rebase-drop-noninteractive/SKILL.md) —
   invoked as the `GIT_SEQUENCE_EDITOR` (Mode A). Its
   `scripts/write-drop-todo.py` receives the target SHA list (via
   `--action drop` / `--action edit` / `--action reword` remap) and rewrites
   the todo non-interactively.
2. [`git-commit-replace-and-replay`](../git-commit-replace-and-replay/SKILL.md) —
   Mode B mechanics: `prepare` / `finish` / `verify` for the
   dedicated-worktree in-place route.
3. [`git-worktree-state-fingerprint`](../../audit/git-worktree-state-fingerprint/SKILL.md) —
   Gates 1 and 8: byte-level capture/compare replaces the previously
   prose-only baseline pipeline.
4. [`git-submodule-history-classification`](../../../../git/submodule/repair/git-submodule-history-classification/SKILL.md)
   — optional scoping input: its `scripts/classify-submodule-commits.py`
   locates the INTRO commit when the target is a submodule path, and its
   post-rebase zero-commits result is the verification evidence.

The composer's domain-specific value-add: the isolated-worktree lifecycle
(Mode A) and the dedicated-worktree in-place lifecycle (Mode B), both under
a dirty-worktree-preservation contract that none of the bases provides. The
core constraint: the current working tree MUST NOT be touched — proven by
byte/index-level baseline comparison, not a status string (see Gate 1 and
Gate 8).

Bidirectional discoverability: the bases list this composer in their
`## Composition by Higher-Level Skills` tables.

## Related Skills

- [`git-commit-edit`](../../../../git-commit-edit/SKILL.md) — in-place
  single-commit interactive editing; this composer is its worktree-isolated,
  dirty-tree-safe counterpart.
- [`git-pre-execution-safety-stash`](../../../../git-pre-execution-safety-stash/SKILL.md) —
  the canonical apply-not-pop safety stash used at Gate 3 when additional
  working-tree protection is required.

## Modes

- **Mode A — scratch-worktree isolation** — the working tree is never
  touched; the edit happens in a scratch worktree on a `rebase-<purpose>`
  branch; gates 3–8 run as today, now scripted (todo writer + fingerprint
  gates). Use when the cwd is the MAIN worktree or when strict
  isolation is required.
- **Mode B — dedicated-worktree in-place** — the proven in-place route, used
  when the cwd IS a dedicated linked worktree (e.g.
  `…-worktrees/<name>`): skip the scratch worktree; mechanics delegate to
  [`git-commit-replace-and-replay`](../git-commit-replace-and-replay/SKILL.md);
  dirty state survives via `--autostash`; proof = fingerprint gates +
  range-diff parity.

> **Prohibition:** Mode B MUST NOT be used in the main worktree — the
> delegated `prepare` refuses when `--git-dir` equals `--git-common-dir`
> unless explicitly overridden; never override it.

## Environment & Dependencies

| Requirement | Version | Notes |
| ----------- | ------- | ----- |
| Python | 3.12+ | For `scripts/plan-commit-edit.py` and the delegated base scripts — stdlib only |
| Bash | 3.2+ (macOS) | For `scripts/isolate-edit-worktree.sh` — `set -euo pipefail` |
| Git | 2.x | `worktree`, `rebase -i`, `rebase --onto`, `reset --soft` |

## Scripts

### `scripts/plan-commit-edit.py` — deterministic discovery half

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `--repo <path>` | no | Repo root (default `.`). |
| `<target-sha>` | yes | Full or abbreviated commit SHA to edit. |
| `--action <drop\|edit\|reword>` | no | Todo action (default `drop`). |
| `--mode <scratch\|in-place>` | no | Isolation mode (default `scratch`). |
| `--purpose <name>` | no | Purpose token for branch/worktree naming. |
| `--json` | no | Emit the plan as JSON. |

Emits (scratch mode): `mode`, `repo`, `target_sha` (fully resolved),
`action`, `base_ref` (`<target>^`), `branch_name` (`rebase-<purpose>`),
`backup_branch` (`backup/pre-edit-<purpose>`), `worktree_path`
(`<repo>/scratch/rebase-<purpose>`), `sequence_editor` (absolute path to the
sibling base's `write-drop-todo.py` — resolved relative to this script's own
location, so invocation works regardless of `cwd`), and `sequence_args`.
In-place mode instead emits `mode`, `repo`, `target_sha`, `action`,
`branch`, `backup_branch`, and `pre_tip` (no worktree/sequence-editor
fields). Exits `1` if the base script is missing (scratch mode), the SHA
does not resolve, or in-place mode runs on a detached HEAD.

### `scripts/isolate-edit-worktree.sh` — CRUD orchestration

```text
--repo <path> --worktree-path <path> --branch <name> --base-ref <ref> --target-sha <sha> --sequence-editor <path> [--action drop|edit]
```

Note: for long drop lists with multiple SHAs, `--target-sha` accepts multiple
space-separated SHAs (pass the full list as one quoted argument).

Performs: `git worktree add -b <branch> <worktree-path> HEAD`, then inside
the worktree runs the scripted rebase (`GIT_SEQUENCE_EDITOR` + `GIT_EDITOR=true`),
then prints the new tip. Conflict resolution and cleanup are prose gates
below, not script steps.

## Protocol

> **Core constraint:** the current working tree MUST NOT be touched. Gates 1
> and 8 prove this with content-level evidence, not a status string.

1. **Baseline gate** — capture, BEFORE anything, the byte-level fingerprint:
   `python3 <path>/scripts/worktree-state-fingerprint.py capture --repo
   <target-worktree> --out <scratch>/baseline-pre.json` (porcelain, index,
   staged diff, worktree diff, untracked hashes). The protocol MUST end with
   all of them byte-identical except the documented expected deltas (Gate 8).
2. **Plan gate** — `python3 <path>/scripts/plan-commit-edit.py <sha>
   [--mode scratch|in-place] [--action ...] [--purpose ...]`; show the
   intended operation (drop / edit / reword), the base ref and scratch
   worktree path (Mode A) or the branch + pre-tip (Mode B), and the todo
   scrub / replacement target to the user.
3. **Safety/backup gate** — `git branch backup/pre-edit-<purpose>` at the
   current HEAD. Mode A additionally: `git worktree add -b rebase-<purpose>
   <repo>/scratch/rebase-<purpose> HEAD`. Optionally also capture an
   apply-not-pop safety stash per
   [`git-pre-execution-safety-stash`](../../../../git-pre-execution-safety-stash/SKILL.md).
4. **Isolate/rebuild gate** —
   - *Mode A*: inside the worktree, run `scripts/isolate-edit-worktree.sh`
     (which wraps the `GIT_SEQUENCE_EDITOR`-scripted `git rebase -i
     <base-ref>` from
     [`git-rebase-drop-noninteractive`](../git-rebase-drop-noninteractive/SKILL.md)).
   - *Mode B*: `replace-and-replay.py prepare --repo <worktree> --target
     <sha> --state-out <scratch>/state.json` (refuses the main worktree).
5. **Amend/reword/edit gate** —
   - *Mode A*: for `edit` stops: amend content and `git rebase --continue`;
     for conflicts: resolve, `git add`, then `GIT_EDITOR=true PAGER=cat git
     rebase --continue`. NEVER `git commit --amend` on a conflicted commit
     before continuing (it folds the staged resolution into the WRONG
     commit — see the base's pitfall table).
   - *Mode B*: stage the edit, then `replace-and-replay.py finish --state
     <state.json>` (`--message` / `--author` for rewords).
6. **Interruption recovery** —
   - *Mode A*: `git commit -C <sha>` (recreate the interrupted strip), then
     `GIT_EDITOR=true PAGER=cat git rebase --continue`.
   - *Mode B* conflict: resolve, `git add`, `GIT_EDITOR=true git rebase
     --continue`, then re-run `verify` — post-conflict replays report
     REVIEW_NEEDED by design (review the interdiff).
7. **Tree-check gate** — `git diff --stat backup/pre-edit-<purpose> HEAD`
   shows ONLY the intended files; ADD the stack-level parity proof:
   - *Mode A*: `git range-diff <target>^..<backup-tip> <target>^..HEAD` —
     apply the marker-accounting rule (all commits accounted, balanced
     `<`/`>`, at most ONE changed commit) from
     [`git-commit-replace-and-replay`](../git-commit-replace-and-replay/SKILL.md)
     § Expected Range-Diff Markers.
   - *Mode B*: `replace-and-replay.py verify --state <state.json>` (runs
     automatically after `finish`).
8. **Fast-forward gate** —
   - *Mode A*: on the main worktree `git reset --soft rebase-<purpose>`;
     then capture post and `worktree-state-fingerprint.py compare --pre
     <scratch>/baseline-pre.json --post <scratch>/baseline-post.json`:
     porcelain / diffs / untracked IDENTICAL + `head` = expected new tip;
     every other delta (e.g. index-blob refresh on gitlink repos) MUST be
     individually explained or STOP.
   - *Mode B*: no fast-forward — the worktree's branch IS the target branch;
     capture post and compare with the same expected-delta policy.
9. **Cleanup gate** (after confirmation) — `git worktree remove
   <worktree-path>` (Mode A), delete `backup/pre-edit-<purpose>` and
   `rebase-<purpose>` only after the user confirms the rewritten branch is
   verified. `git branch -d` refuses post-rewrite tips — use `-D`
   deliberately. Skip the push when the branch has no upstream (record the
   no-upstream state instead).

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| -------- | --------------------- |
| [`git-submodule-history-removal`](../../../../git/submodule/lifecycle/git-submodule-history-removal/SKILL.md) | Delegates its Isolate/Rebase/Fast-forward gates to this composer's protocol, passing the INTRO (+ optional POINTER-UPDATE) SHA list as the drop targets and consuming the Gate-8 baseline match as its own verification evidence. |

## Prohibited Behaviors

- **Running the rebase in the main worktree** — always the isolated worktree
  (Mode A) or a dedicated linked worktree (Mode B; `prepare` refuses the
  main worktree — never override the refusal).
- **Proceeding past Gate 8 on any baseline mismatch** — staged resurrection
  of removed gitlinks is the canonical silent-failure mode.
- **`git reset --hard`** — the fast-forward is `reset --soft` by design;
  hard reset destroys user work.
- **Deleting the backup branch or worktree without user confirmation** —
  cleanup is a separate authorization gate.
- **Pushing** — push (`--force-with-lease`) is owned by the submodule-removal
  composer's push gate, not by this skill.

## Common Pitfalls

| Pitfall | Solution |
| ------- | -------- |
| `fatal: '<branch>' is already used by worktree at ...` | The branch name is taken — pick a fresh `--purpose` token. |
| Old index shows removed submodule as staged addition after `reset --soft` | Expected on the OLD base; resolve by migrating the dirty worktree onto the new base deliberately (preservation branch / index-preserving stash), never by committing the staged addition. |
| Rebase stops on `.gitmodules` conflict | Resolve, `git add .gitmodules`, `GIT_EDITOR=true git rebase --continue`. |
| `git commit --amend` mid-rebase after conflict resolution | Forbidden — it rewrites the previously-applied commit. Use `git rebase --continue`. |
| `git branch -d` refuses the post-rewrite tip | Expected after a history rewrite — use `-D` deliberately, only after parity verification and user authorization. |
| Push attempted on a branch with no upstream | Record the no-upstream state instead; do not push. |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
