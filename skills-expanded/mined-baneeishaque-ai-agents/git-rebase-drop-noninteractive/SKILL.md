---
name: git-rebase-drop-noninteractive
description: >-
  Base primitive — run a git rebase that drops or edits named commits without
  any interactive editor, by generating the rebase todo list programmatically
  (GIT_SEQUENCE_EDITOR). Idempotent todo rewrite, --check mode,
  interrupted-rebase recovery, keep-empty guard, optional pick→edit remap.
category: Git & Repository Management
---

# Git Rebase Drop Non-Interactive (v1)

> **Name:** git-rebase-drop-noninteractive<br>
> **Description:** Base primitive — scripted, non-interactive rebase todo
> rewrite (pick → drop / edit) via `GIT_SEQUENCE_EDITOR`<br>
> **Category:** Git & Repository Management

## Composition Rationale

This skill is a base primitive: the rebase-todo rewrite is a deterministic,
byte-exact text transform reused by every higher-level workflow that drops or
edits named commits from history without an interactive editor. Composers
would otherwise re-derive the todo-rewrite logic ad hoc, splitting the SSOT.
Known composer:

- [`git-commit-edit-in-worktree`](../git-commit-edit-in-worktree/SKILL.md) —
  shells out to `scripts/write-drop-todo.py` as its `GIT_SEQUENCE_EDITOR`
  inside an isolated worktree.

## Related Skills

- [`git-commit-edit`](../../../../git-commit-edit/SKILL.md) — interactive
  single-commit editing; this base is its non-interactive, multi-commit,
  worktree-safe counterpart.
- [`git-rebase-standardization`](../../../../git-rebase-standardization/SKILL.md) —
  commit-action mapping for rebase chains; this base executes the DROP/EDIT
  actions without an editor.

## Environment & Dependencies

| Requirement | Version | Notes |
| ----------- | ------- | ----- |
| Python | 3.12+ | Stdlib only — no pip dependencies |
| Git | 2.x | For the invoking `git rebase -i` |

## CLI Contract

`scripts/write-drop-todo.py`:

| Argument | Required | Description |
| -------- | -------- | ----------- |
| `<todo-file>` | yes | Path to the rebase todo file. Git appends it as the LAST argument via `GIT_SEQUENCE_EDITOR`; direct invocations may pass it first — both orders are accepted (the positional that exists on disk is treated as the todo). |
| `<sha>...` | yes (≥ 1) | Full or abbreviated commit SHAs to drop / turn into `edit`. |
| `--edit <sha>...` | no | Instead of `drop`, rewrite `pick <sha> → edit <sha>` (amend / reword / squash-scratch use case). Repeatable. A SHA passed in both the positional list and `--edit` is edited — `--edit` wins. |
| `--check` | no | Do not write; exit 1 if any named SHA is absent from the todo file, 0 otherwise. |
| `--dry-run` | no | Print the rewritten todo to stdout; do not modify the file. |

**Behavior:**

- Rewrites every `pick <sha> …` line whose SHA is in the target set; default
  `→ drop <sha>`; with `--edit <sha>`, `→ edit <sha>` (`--edit` wins over the
  positional drop set).
- SHA matching is prefix-tolerant: the todo file usually carries abbreviated
  SHAs (`pick 2da761c …`) while callers pass full SHAs — either side may be
  the abbreviation. A todo SHA matching more than one distinct target aborts
  with an ambiguity error before any write.
- Idempotent: lines already in the target state (drop of a to-dropped SHA;
  edit of a to-edited SHA) are skipped.
- Preserves all other lines byte-exact (reword/squash/fixup, comments,
  blanks, CRLF/LF).
- `--check`: 1 if any target SHA is NOT found anywhere in the todo file; 0
  if all present.
- Exit codes: `0` success; `1` `--check` failure or validation; `2` usage.

## Protocol

**Invocation** (exact form — SHA list is a `GIT_SEQUENCE_EDITOR` argument):

```bash
GIT_SEQUENCE_EDITOR='python3 <path-to-skill>/scripts/write-drop-todo.py fdc018e... aa1023a...' \
GIT_EDITOR=true PAGER=cat git rebase -i <base-ref>
```

1. **Pre-flight guard** — run `PAGER=cat git status --porcelain`. If the
   working tree is dirty, this base only notes it: the composer
   [`git-commit-edit-in-worktree`](../git-commit-edit-in-worktree/SKILL.md)
   NEVER runs an in-place rebase on the main worktree. This base is only ever
   executed inside an isolated worktree.
2. **Todo rewrite** — invoke the rebase with the `GIT_SEQUENCE_EDITOR`
   environment variable pointing at `scripts/write-drop-todo.py` with the
   target SHAs; git hands the script the todo file path as its last argument.
3. **Empty-commit policy** — `--keep-empty` is handled by the caller; the
   default (unless explicitly passed) is the git default (drop empty commits).
4. **Interrupted-apply recovery** — when a rebase stops on a conflict or an
   interruption:

   ```bash
   git commit -C <sha>          # recreate the interrupted strip
   GIT_EDITOR=true PAGER=cat git rebase --continue
   ```

5. **`.gitmodules` conflict resolution** — when the dropped commit removed or
   added a submodule and a later commit conflicts on `.gitmodules`: resolve
   the conflict file, `git add .gitmodules`, then
   `GIT_EDITOR=true PAGER=cat git rebase --continue`.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| -------- | --------------------- |
| [`git-commit-edit-in-worktree`](../git-commit-edit-in-worktree/SKILL.md) | Invokes `scripts/write-drop-todo.py <sha>... [--edit <sha>...]` via `GIT_SEQUENCE_EDITOR` for the todo-write stage of its isolated-worktree rebase; consumes the exit code (0 = todo applied, 1 = `--check` failure) as a gate. |
| [`git-submodule-history-removal`](../../../../git/submodule/lifecycle/git-submodule-history-removal/SKILL.md) | Indirect — drives the drop-rebase through `git-commit-edit-in-worktree`, which calls this base's script with the classified INTRO / POINTER-UPDATE SHA list. |

## Prohibited Behaviors

- **Running the rebase in the main worktree when it is dirty** — the todo
  rewrite is safe anywhere, but the rebase itself MUST happen in an isolated
  worktree (see the composer).
- **Rewriting todo lines whose SHA is not in the target set** — other
  actions (reword / squash / fixup / exec) are preserved byte-exact.
- **Emitting diagnostics on stdout** — the script prints only the rewritten
  todo (`--dry-run`) or nothing; errors go to stderr.

## Common Pitfalls

| Pitfall | Solution |
| ------- | -------- |
| SHA not found in the todo (already rewritten, wrong base, or abbreviated too aggressively) | Run with `--check` first — exits 1 with the absent SHA(s) before any file mutation. |
| Caller passes full SHAs while the todo file holds abbreviated ones | Since v1.0.1 matching is prefix-tolerant — full vs abbreviated on either side both work; never exact-match. |
| Dropping a commit that introduces a submodule whose path is re-created later | `add/add` conflict on the path; resolve per the divergent-recreation protocol in [`git-drop-commit-with-divergent-recreation`](../../../../git-drop-commit-with-divergent-recreation/SKILL.md). |
| `.gitmodules` conflict during continue | Resolve, `git add .gitmodules`, then `GIT_EDITOR=true git rebase --continue`. |
| Rebase interrupted by a stop | `git commit -C <sha>` + `GIT_EDITOR=true git rebase --continue`. |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
