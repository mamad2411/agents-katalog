---
name: ralph-plan
description: >-
  use this when a goal must become a Ralph plan before the loop
  runs — topic branch, scoped items, runtime_contract, clean
  worktree, planner cannot touch implementation files
license: MIT
metadata:
  portability: portable
---
# ralph-plan

Turn a goal into durable Ralph state. The planner writes `.ralph/` only.
The engine (or you) commits the plan after a gate. Do not start
`ralph-loop` until this file set exists and the worktree is clean.

## When

- A goal must become a Ralph plan before the loop runs.
- The loop cannot start until the four `.ralph/` files exist and the
  worktree is clean.

## Preconditions

- Branch matches `ralph/<topic>`. Never plan on the default branch.
- Worktree is clean (`git status --porcelain` empty).
- No live Ralph lock. If `.git/ralph.lock` exists, inspect the recorded
  pid. Do not delete it while that process is alive.

## What the planner may touch

Only:

- `.ralph/plan.md` — objective + invariants
- `.ralph/items.json` — runtime_contract + items
- `.ralph/loop.md` — reset to `running: false`, `iteration: 0`, `stop_reason: null`
- `.ralph/progress.md` — replace with one timestamped plan-created entry

Anything else is a failed plan. Restore the last verified tree.

## Plan shape

`plan.md` states the objective and the non-negotiable invariants.

Each item in `items.json`:

- `id` kebab-case, unique
- `category`
- `passes: false`, `blocked: false` (unless owner-only / env-gated — then `blocked: true`)
- `allowed_paths` — exact files, or directory prefixes ending in `/`
- `description`, concrete `steps`, `regression_notes`
- small enough that the repo gate can verify it alone

Example item (documented fields only):

```json
{
  "id": "wire-checkout-button",
  "category": "ui",
  "passes": false,
  "blocked": false,
  "allowed_paths": ["src/checkout/"],
  "description": "Wire the checkout button to the cart total.",
  "steps": ["Add the click handler", "Run the gate"],
  "regression_notes": "Re-run if the cart total changes."
}
```

`runtime_contract` stays this shape:

- `verification_gates` — commands the engine re-runs outside the worker
- `require_one_item_per_iteration: true`
- `require_commit: true`
- `require_progress_append: true`
- `never_push_without_owner_ok: true`
- `branch` — the current `ralph/<topic>`
- `protected_paths` — engine, prompt, gate, plan files the worker must not edit

## How

1. Confirm branch + clean tree.
2. Read the repo only. Git writes are forbidden during planning.
3. Write the four `.ralph/` files above.
4. Snapshot ignored sensitive files (`.env`, tokens, keys). If they change,
   abort and restore.
5. Build a candidate tree of those four files. Run the gate in a
   **detached worktree** of that tree. Require exit 0 and final line
   `ALL GATES PASS`. The gate must not dirty the tree.
6. Commit hook-free (`commit-tree` / equivalent) from the verified tree.
   Leave the worktree matching that commit.
7. Stop. The loop is a later session (`ralph-loop`).

## Anti-patterns

- Planning on `main`.
- Planner editing implementation files "to get a head start."
- Planner committing, pushing, or switching branches.
- Items without `allowed_paths` or with `/` / `..` in a path.
- One mega-item that is the whole goal.
- Leaving `loop.md` running from a previous attempt.

## Related

ralph-loop · ralph-swarm · to-spec · quality-loop
