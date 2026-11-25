---
name: git-commit-replace-and-replay
description: >-
  Base primitive — deterministically replace a single Git commit in place and
  replay its descendants with `git rebase --autostash --onto`, then verify
  patch parity via range-diff. No sequence editor, no todo writer, no
  interactive stop.
category: Git & Repository Management
---

# Git Commit Replace and Replay (v1)

> **Name:** git-commit-replace-and-replay<br>
> **Description:** Base primitive — deterministic in-place single-commit replacement + range-diff parity verification<br>
> **Category:** Git & Repository Management

## Composition Rationale

This skill is a base primitive: the session-proven in-place replacement route
(detach at target → amend → `git rebase --autostash --onto <new> <target>
<branch>` → range-diff parity check) was previously undocumented and had to
be re-derived ad hoc. The route avoids the three failure modes of interactive
replacement: no sequence editor is launched, no rebase-todo writer is needed,
and there is no interactive stop — the `--onto` replay is a deterministic
one-shot operation. Known composers/consumers:

- [`git-commit-edit-in-worktree`](../git-commit-edit-in-worktree/SKILL.md) —
  Mode B (dedicated-worktree in-place) delegates its mechanics to this
  script's `prepare`/`finish`/`verify`.
- Future adopters (out of current scope):
  [`git-commit-message-reword`](../../../../git-commit-message-reword/SKILL.md)
  and
  [`git-commit-identity-rewrite`](../../../../git-commit-identity-rewrite/SKILL.md)
  can reuse the same primitive for non-interactive reword/identity edits.

## Related Skills

- [`git-commit-edit`](../../../../git-commit-edit/SKILL.md) — interactive
  in-place edit routes (rebase todo + sequence editor); use when the edit is
  interactive or spans multiple commits.
- [`git-rebase-drop-noninteractive`](../git-rebase-drop-noninteractive/SKILL.md)
  — scripted rebase-todo writer for drop/edit routes; this skill needs no
  todo writer.
- [`git-pre-execution-safety-stash`](../../../../git-pre-execution-safety-stash/SKILL.md)
  — recoverable safety snapshot before the replacement.

## Environment & Dependencies

| Requirement | Version | Notes |
| ----------- | ------- | ----- |
| Python | 3.12+ | Stdlib only — no pip dependencies |
| Git | 2.26+ | Merge-backend rebase; range-diff subcommand required |

## CLI Contract

[`scripts/replace-and-replay.py`](scripts/replace-and-replay.py):

| Subcommand | Arguments | Description |
| ---------- | --------- | ----------- |
| `prepare` | `--repo <path> --target <sha> [--branch <name>] [--allow-main-worktree] --state-out <state.json>` | Resolves target/branch, refuses the main worktree unless allowed, detaches HEAD at the target, writes the state JSON. |
| `finish` | `--state <state.json> [--message <msg>] [--author "<name <email>>"]` | Amends the target (staged content and/or message/author), replays the branch with `--autostash --onto`, then auto-runs `verify`. |
| `verify` | `--state <state.json>` | Range-diff parity check; prints verdict, commit count, and `diff --stat`. |

**Exit codes:** `0` ok / PARITY_OK; `2` usage, git error, or state mismatch;
`3` replay conflict (resolve → `git add` → `git rebase --continue` → `verify`);
`4` REVIEW_NEEDED (range-diff shape outside the accepted parity shapes).

**State JSON:**

```json
{
  "schema_version": 1,
  "repo": "<abs path>",
  "worktree": "<abs path>",
  "target_sha": "<full sha>",
  "branch": "t1",
  "pre_tip": "<full sha>",
  "prepared_at": "<ISO-8601>"
}
```

`finish` additively records `new_sha` and `new_tip` after a successful replay.

## Protocol

1. **Prepare** — from a dedicated linked worktree:

   ```bash
   python3 .agents/skills/git/basic/edit/git-commit-replace-and-replay/scripts/replace-and-replay.py \
     prepare --repo <worktree> --target <sha> --state-out <scratch>/state.json
   ```

2. **Edit** — modify the worktree and `git add` the change (content edit), or
   plan a reword/author change (no staged content needed).
3. **Finish** — `finish --state <state.json>` (add `--message`/`--author` for
   rewords). The amend is `git commit --amend --no-edit` by default; a
   reword-only run (nothing staged) REQUIRES `--message` or `--author`.
4. **Verify** — runs automatically after a successful replay; re-run
   `verify --state <state.json>` any time. Dirty tracked state survives the
   replay via `--autostash`; untracked files are untouched.

## Expected Range-Diff Markers

`verify` runs `git range-diff <target>^..<pre_tip> <target>^..<new_tip>` and
requires full marker accounting (N = old-side commit count):

| Marker | Meaning |
| ------ | ------- |
| `=` | Patch and message identical. |
| `!` | Changed commit, paired — small relative content edits, rewords, or context-shifted descendants. |
| `<` + `>` | Changed commit, unpaired — total-rewrite heuristic for large relative edits and file-creation patches. |

Verdict PARITY_OK requires: every old-side commit accounted for
(`eqs + bangs + lt == N`), balanced unpaired markers (`lt == gt`), and at
most ONE changed commit (`bangs + lt <= 1`) — the replaced target. Any other
shape yields REVIEW_NEEDED (exit 4) with the raw range-diff for human
review, including: extra changed commits (descendants whose patch context
overlaps the replaced region), post-conflict resolutions, or unbalanced
accounting.

## Autostash Semantics

`--autostash` stashes tracked modifications before the replay and restores
them after. Consequences:

- Uncommitted tracked changes survive a successful replay.
- On conflict, the autostash is re-applied after you finish the rebase —
  expect the dirt back, not lost.
- Untracked files are never stashed and never touched by the replay.

## When to Use This vs Alternatives

| Situation | Route |
| --------- | ----- |
| Single-commit content edit / reword / author change, non-interactive | **This skill** |
| Interactive edit, multi-commit edit, or history browsing during edit | [`git-commit-edit`](../../../../git-commit-edit/SKILL.md) |
| Scratch-worktree isolation + full gate suite (fingerprint, backup branch) | [`git-commit-edit-in-worktree`](../git-commit-edit-in-worktree/SKILL.md) Mode A |
| The session cwd IS a dedicated linked worktree | [`git-commit-edit-in-worktree`](../git-commit-edit-in-worktree/SKILL.md) Mode B → delegates here |

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| -------- | --------------------- |
| [`git-commit-edit-in-worktree`](../git-commit-edit-in-worktree/SKILL.md) | Mode B replaces its interactive isolate/amend/replay steps with `prepare` + `finish`; Gate 8 pairs this skill's `verify` with [`git-worktree-state-fingerprint`](../../audit/git-worktree-state-fingerprint/SKILL.md) capture/compare for byte-level proof. |

## Prohibited Behaviors

- **Running in the main worktree** — `prepare` refuses when
  `--git-dir` equals `--git-common-dir` unless `--allow-main-worktree` is
  passed explicitly; the default route is a dedicated linked worktree.
- **Pushing** — this skill never pushes; force-push authorization is a
  separate, explicit user gate.
- **Hand-editing the state JSON** — `pre_tip`/`target_sha` are the parity
  contract.
- **Multi-commit replacement** — one target per state file; chain states for
  more.

## Common Pitfalls

| Pitfall | Solution |
| ------- | -------- |
| Reading the `<`/`>` pair as an anomaly | It is a valid shape for the single changed commit — file-creation patches and large relative edits produce it. See Expected Range-Diff Markers. |
| Descendant flagged changed though its edit is intact | Its patch context overlaps the replaced region — range-diff cannot prove identity; REVIEW_NEEDED asks for a manual interdiff review. |
| Expecting PARITY_OK after a conflict resolution | Resolutions alter descendant patches by definition — verify reports REVIEW_NEEDED (exit 4); review the interdiff and confirm the descendant changes are semantically preserved. |
| Forgetting to stage the edit before `finish` | `finish` errors when nothing is staged and no `--message`/`--author` is given. |
| Color codes polluting range-diff parsing | The script always runs `git -c color.ui=never range-diff`. |
| User config altering replay behavior | The replay pins `-c rebase.autoSquash=false -c rebase.rebaseMerges=false` for determinism. |
| Root-commit target | `verify` reports REVIEW_NEEDED — the range-diff base `<target>^` does not exist for a root commit; review manually. |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).
