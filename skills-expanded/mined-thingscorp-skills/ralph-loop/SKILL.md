---
name: ralph-loop
description: >-
  use this when a ticket queue must be worked across sessions — run the
  self-verifying Ralph loop: one item per iteration, gate outside the
  worker, commit only from a verified tree on a topic branch
license: MIT
metadata:
  portability: portable
---
# ralph-loop

Execute a queue of vertical tickets across sessions with a self-verifying
loop. Live agent context is disposable. Durable state lives in `.ralph/`
(plan, items, prompt, loop state, progress log). One iteration completes
exactly one item.

## When

- A to-spec ticket queue (or any discrete item list) must be worked to done
  across sessions without losing state.
- ralph-plan produced the verified plan and items; this loop executes them.
- Each item needs independent verification before it lands.
- When a grill-execute-clear feature outgrows one session, graduate its
  mini-spec to to-spec, then run the resulting tickets here.

## Durable files

| File | Owns |
|---|---|
| `.ralph/plan.md` | objective + invariants |
| `.ralph/items.json` | ordered items + `runtime_contract` |
| `.ralph/prompt.md` | worker contract for each fresh agent |
| `.ralph/loop.md` | run state — **engine only** |
| `.ralph/progress.md` | append-only evidence |

`runtime_contract` must declare: `verification_gates`, `branch` (topic),
`protected_paths`, `require_one_item_per_iteration`, `require_commit`,
`require_progress_append`, `never_push_without_owner_ok`.
Each item declares `allowed_paths`, `passes`, `blocked`.

Plan first: replacing the plan and items **resets** `loop.md` and
`progress.md`. Do not start a loop against a stale plan.

## The loop (engine protocol)

You are the engine. A fresh subagent is the worker for each item.
Never let the worker verify its own work. Re-read all durable state before
every iteration.

1. Read `.ralph/loop.md`, `items.json`, `plan.md`, `prompt.md`, `progress.md`.
2. Confirm you are on the contract topic branch. If not, stop. Never touch
   the default branch.
3. Optionally run a work-select gate. Review means the engine picks. Gate
   error means FIFO (`passes:false`, `blocked:false`) stands.
4. Take the lock (`.git/ralph.lock`). Do **not** auto-reclaim a stale lock —
   inspect and remove it only after the recorded process has stopped.
   Mark the item running. Stop if nothing actionable remains.
5. Spawn ONE fresh worker for that item only, with the worker contract below.
6. When the worker returns:
   - Save the candidate as an **immutable Git tree**.
   - Run the saved baseline gate and the **current** gate **outside** the
     worker, in a detached worktree of that exact tree.
   - Scope-check the diff against `allowed_paths`. Reject `protected_paths`.
   - Acceptance: exit 0 **and** final line `ALL GATES PASS`.
   - On pass: commit **hook-free** from that same verified tree (Git plumbing,
     not `git commit` that hooks can rewrite). Set `passes: true`. Append an
     engine progress entry. Release the lock.
   - On fail or stop: write `refs/ralph/recovery/<item>-<timestamp>`, restore
     the last verified branch state, record the stop reason, release the lock.
     Do not leave a dirty default branch behind.
7. If the worker claims `blocked: true`, judge the claim before honoring it.
   Send-back means respawn with a hint. Owner-only access → stop and report.
8. After each iteration decide continue vs stop. Thrashing → escalate.

## Worker contract

Hand the worker these rules. The engine also enforces them after the fact.

- Complete exactly one selected item.
- Change only that item's `allowed_paths` plus one progress append.
- Work only on `runtime_contract.branch`.
- Run the gate. Require exit 0 and final line `ALL GATES PASS`.
- Never set `passes: true`. The engine sets it after both gates pass.
- `blocked: true` only for a real external blocker.
- Append exactly one timestamped progress entry (item id, summary, gate
  result, `Outcome: PASS` or `Outcome: BLOCKED`).
- Do not commit, switch branches, merge, rebase, reset, or push.
- Do not edit `.ralph/loop.md`.
- No generated-by attribution in code or commits.
- Never commit secrets, tokens, or `.env` files.

Kill the whole worker process group when the iteration ends or times out
(SIGTERM, then SIGKILL). Do not leave orphaned children.

## Optional judgment gates

Small semantic questions (select, verify, triage, blocker, continue) can be
asked by a judgment helper so the frontier model doesn't have to. Code owns
the workflow; the helper only supplies judgments. Gate exits: 0 acted,
1 review (engine decides), 2 escalate to the owner, 3 gate error — on error
fall back to the pre-helper behavior and say so. Branch only on typed
answers, never on free-form text.

## Rules

- One item per iteration. No batching, no drive-bys.
- Two gates: baseline + current. Both outside the worker.
- Commit only from the verified tree, hook-free.
- Never push, merge, force-push, or change the default branch.
- Failed verification is a failed iteration plus a recovery ref.

## Anti-patterns

- Letting the worker verify its own work.
- Committing the worker's output without the engine-side gate rerun — the engine re-runs baseline + current gates outside the worker before any commit.
- Spawning a worker without handing it the worker contract.
- `git commit` on a dirty index so hooks can rewrite the tree you gated.
- Auto-deleting `.git/ralph.lock` because it "looks stale."
- Linked worktrees that share a Git dir with another lane.
- Starting the next iteration while the lock is still held.
- Touching `main` / `master` because the topic branch "is almost done."

## Related

ralph-plan (verified plans + items, the upstream) · to-spec · ralph-swarm · grill-execute-clear · handoff · compact · quality-loop
