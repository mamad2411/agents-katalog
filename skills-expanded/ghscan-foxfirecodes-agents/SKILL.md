---
name: split-branch
description: Split a large branch into a stack of smaller, individually tested GitButler branches — including splitting single files into sequences of incremental commits. Use when the user asks to split, break up, or restack a big branch or diff into smaller reviewable branches/commits.
---

# Split a Branch into a Tested Stack

Split one large branch into stacked smaller branches where every commit compiles, passes tests, and is functional on its own, and the final commit's tree is byte-identical to the original branch's final state.

Load and follow the `gitbutler` skill for all version-control operations. This skill defines the workflow and sequencing; the `but` quick reference at the bottom resolves ambiguity for the specific commands this workflow needs.

## Core invariants

1. **The working tree is always the stack tip.** Intermediate versions of a file are committed by writing that version's full content into the working tree and committing it — never by hunk-juggling or history insertion.
2. **Test only at the tip.** A state is testable exactly when it is the working tree. Author each reduced state and test it in the same step, before any real history exists.
3. **History is only written from proven states.** The rebuild phase copies already-tested file snapshots; it makes no creative decisions.
4. **The final state is restored mechanically** from the byte-exact snapshot taken up front. End-state parity is by construction, never by re-derivation.
5. Never build top-down by inserting commits below existing ones (`--before` + conflict resolution) — the tip stays at final state, so intermediates are never testable, and each fix cascades conflicts upward.

## Interaction protocol

1. **Intake.** The user names the branch. Read its full diff (and any related uncommitted changes) and reply with a one-paragraph summary of what the branch does. Ask whether uncommitted changes belong in scope.
2. **Seams.** The user either specifies the seams (branch/commit boundaries) or asks to discuss; in discussion, propose seams with a one-line rationale each and iterate until the user settles them.
3. **Plan.** Spawn a planning subagent to design the concrete _incremental changes_: for each stage, which files change, what the reduced version contains, what functionality is present, and what is deferred to later stages — not merely which files appear in which commit. Present a per-stage summary to the user.
4. **Approval gate.** Iterate on the plan until the user approves. Do not run any mutating command before explicit go-ahead.
5. **Execute** phases below, delegating stage implementation to subagents. After each stage, report: stage name, tests run and results, and any deviations from the plan needed to pass tests or make functional sense.
6. **Pause only for major blockers** that genuinely require user input (destructive recovery, seam changes that alter the approved plan's shape). Otherwise run to completion.

## Execution

Maintain a persistent plan/progress file in the scratchpad (stages, per-stage status, deviations) so the run survives context compaction. State snapshots live in scratchpad directories: `states/final/`, `states/<NN>-<stage>/`, each containing the full content of _every_ touched file at that state, plus a manifest listing deletions and renames.

### Preflight

1. `but pull`; resolve any conflicts.
2. Consolidate scope so the workspace tip is the complete final state: squash the source branch to one commit and amend in any in-scope dirty changes. Park or leave out-of-scope dirty changes untouched.
3. Run the relevant test suites (use the project's standard commands per its CLAUDE/AGENTS rules) — they must pass on the final state before splitting. If the environment requires tests to run against the main working tree (e.g. remote-sync tooling like slyncy), all testing in this workflow happens there, never in a linked worktree.
4. Snapshot every touched file to `states/final/` and record the base contents needed for comparison.
5. `but oplog snapshot -m "pre-split: <branch>"` — the single-command eject handle.
6. If other applied branches could interfere with tests, `but unapply` them now and reapply at the end.

### Phase 1 — Descend and test (creative, verified as it goes)

Work backwards from the final state, one stage at a time:

1. Edit the working tree down to the next reduced form (subtract the last remaining stage). Subtraction from a known-good state, not forward-writing from base.
2. Run the stage's test suites against the working tree. Fix until green; fixes here are cheap because no history depends on this state yet.
3. Copy the tested state's touched files to its `states/` directory (with manifest), then `but commit` it onto the tip with message `state <N>: <stage>` — these commits are scaffolding checkpoints only.
4. Repeat until the most-reduced state (stage 1) is tested and saved.

Record every deviation from the plan in the progress file as it happens.

### Phase 2 — Rebuild ascending (purely mechanical)

1. `but oplog restore` to the pre-split snapshot, then flatten to dirty: `but squash <src-branch>` followed by `but uncommit <commit>`. Working tree is again the full final state, uncommitted.
2. For each stage in ascending order: write **all** touched files to that stage's saved content (apply manifest deletions/renames; a file whose content equals base simply produces no diff), then commit to that stage's branch. First commit of a new branch: `but commit <name> -c -m "..."`; the last stage restores files from `states/final/` verbatim.
3. Keep the stack order correct: create each subsequent branch stacked on the previous one (`but branch new <name> -a <prev>` before committing, or run the exact `but move` command GitButler prints on a dependency conflict).
4. If unrelated dirty files exist, pass `--changes` with the stage's file IDs instead of committing everything.

### Phase 3 — Verify by bytes, not by re-testing

1. For every rebuilt commit, compare `git show <sha>:<path>` against the corresponding `states/` file for each touched file — all must be byte-identical. Run this in a cheap verification subagent.
2. Confirm the working tree has zero diff against `states/final/`.
3. If a commit mismatches its state at stage K: `but uncommit` back down through K, rewrite from the saved states, and recommit K upward. Do not amend a mid-stack commit to fix content — the rebase changes the trees above it.
4. Byte-identical trees are the proof of correctness; re-running suites is optional spot-checking, not a requirement.

### Wrap up

Delete leftover scaffolding, reapply any branches unapplied in preflight, and report the final stack (branches, commits, deviations log). Publish only if asked: `but pr new <top-branch> -t` for the whole stack.

## `but` quick reference for this workflow

| Purpose                        | Command                                                           |
| ------------------------------ | ----------------------------------------------------------------- |
| Safety checkpoint / restore    | `but oplog snapshot -m "msg"` / `but oplog restore <snapshot-id>` |
| Update from target             | `but pull`                                                        |
| Flatten branch to one commit   | `but squash <branch>`                                             |
| Make a commit's changes dirty  | `but uncommit <commit-id> --diff`                                 |
| Commit all dirty changes       | `but commit <branch> -m "msg"`                                    |
| Commit selected files          | `but commit <branch> -m "msg" --changes <id>,<id>`                |
| Commit + create branch         | `but commit <name> -c -m "msg"`                                   |
| Create stacked branch          | `but branch new <name> -a <anchor-branch>`                        |
| Stack existing branches        | `but move <child-branch> <parent-branch>`                         |
| Amend tip commit               | `but amend <commit-id> --changes <id>,<id>`                       |
| Inspect IDs / per-commit files | `but status -fv`, `but diff`                                      |
| Publish whole stack            | `but pr new <top-branch-id> -t`                                   |

Commit contents are read from a rebuilt commit with plain read-only git: `git show <sha>:<path>`.
