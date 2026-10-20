---
description: "First-principles analysis to find the strongest solution. Use for architectural decisions, complex tradeoffs, and non-obvious problems."
type: analysis-only
reads: []
stack_categories: []
requires_approval: true
references:
  - .claude/patterns/solve-reasoning.md
branch_prefix: ""
modifies_specs: false
---
Find the optimal solution to a problem using first-principles analysis, structured research, constraint enumeration, self-critique, and convergence.

## Lifecycle

0. Opportunistically clean >24h stale solve worktrees (skips active sessions):
   ```bash
   bash .claude/scripts/lib/clean-stale-worktrees.sh solve
   ```
1. Enter worktree isolation (conditional — only when not already isolated):
   a. Detect existing isolation:
      ```bash
      IN_WORKTREE=$(bash .claude/scripts/lib/in-worktree.sh)
      ```
   b. If `IN_WORKTREE=false`:
      - Call `EnterWorktree` with name `"solve-<current-timestamp>"`
      - On success: run `mkdir -p .runs`; set `WORKTREE_OWNER=true`
      - On failure: continue in current directory; set `WORKTREE_OWNER=false`
   c. If `IN_WORKTREE=true`:
      - Skip `EnterWorktree` (the parent session owns this worktree)
      - Set `WORKTREE_OWNER=false`
2. Run `bash .claude/scripts/lifecycle-init.sh solve`, then merge worktree_owner into the context (reuses init-context.sh's has_identity merge path):
   ```bash
   bash .claude/scripts/init-context.sh solve "{\"worktree_owner\": $WORKTREE_OWNER}"
   ```
3. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh solve)`
   b. If NEXT is "FINALIZE" → go to step 4
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 3a
4. Conditional cleanup (only when this skill owns the worktree):
   ```bash
   OWNER=$(python3 -c "import json; print(str(json.load(open('.runs/solve-context.json')).get('worktree_owner', False)).lower())")
   ```
   If `OWNER=true`:
   a. Run `bash .claude/scripts/lifecycle-worktree-sync.sh`
   b. Call `ExitWorktree` with action `"remove"`
   Else: skip cleanup. The parent session owns the worktree, OR the context predates this fix and may need one-time manual cleanup.

## Do NOT
- Modify any source files — this skill is analysis only
- Create branches or PRs
- Change experiment.yaml or any spec file
- Install or remove packages
- Implement the solution — that is `/change` or `/resolve`'s job
- Propose solutions that require libraries not in experiment.yaml `stack`
