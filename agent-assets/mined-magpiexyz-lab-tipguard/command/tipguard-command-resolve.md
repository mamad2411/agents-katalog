---
description: "Resolve GitHub issues filed against the template: triage, diagnose via first-principles analysis, fix, and validate."
type: code-writing
reads:
  - CLAUDE.md
  - scripts/check-inventory.md
stack_categories: []
requires_approval: true
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/observe.md
  - .claude/patterns/skill-epilogue.md
  - .claude/patterns/solve-reasoning.md
branch_prefix: fix
modifies_specs: false
---
Resolve GitHub issues or refine template quality: $ARGUMENTS

## Modes
- `/resolve #42` — resolve a specific issue
- `/resolve open issues` — resolve all open issues
- `/resolve --refine` — analyze team traces + observation issues to improve template quality

ARGUMENTS: $ARGUMENTS

## Lifecycle

0. Opportunistically clean >24h stale resolve worktrees (skips active sessions):
   ```bash
   bash .claude/scripts/lib/clean-stale-worktrees.sh resolve
   ```
1. Enter worktree isolation (conditional — only when not already isolated):
   a. Detect existing isolation:
      ```bash
      IN_WORKTREE=$(bash .claude/scripts/lib/in-worktree.sh)
      ```
   b. If `IN_WORKTREE=false`:
      - Call `EnterWorktree` with name `"resolve-<current-timestamp>"`
      - On success: run `mkdir -p .runs`; set `WORKTREE_OWNER=true`
      - On failure: continue in current directory; set `WORKTREE_OWNER=false`
   c. If `IN_WORKTREE=true`:
      - Skip `EnterWorktree` (the parent session owns this worktree)
      - Set `WORKTREE_OWNER=false`
2. Run `bash .claude/scripts/lifecycle-init.sh resolve`, then merge worktree_owner into the context (reuses init-context.sh's has_identity merge path):
   ```bash
   bash .claude/scripts/init-context.sh resolve "{\"worktree_owner\": $WORKTREE_OWNER}"
   ```
3. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh resolve)`
   b. If NEXT is "FINALIZE" → go to step 4
   c. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 3a
4. Conditional cleanup (only when this skill owns the worktree):
   ```bash
   OWNER=$(python3 -c "import json; print(str(json.load(open('.runs/resolve-context.json')).get('worktree_owner', False)).lower())")
   ```
   If `OWNER=true`:
   a. Run `bash .claude/scripts/lifecycle-worktree-sync.sh`
   b. Call `ExitWorktree` with action `"remove"`
   Else: skip cleanup. The parent session owns the worktree, OR the context predates this fix and may need one-time manual cleanup.

## Do NOT

- Modify experiment.yaml or other spec files
- Add new features or pages (exception: creating permanent external stack files in STATE 9a is a recurrence-prevention fix)
- Fix things not described in the issues
- Install or remove packages
- Commit to main directly
- Skip validator runs after fixes
- Commit fixes that cause validator regressions
- Apply band-aid fixes that don't address root cause
- Fix only the reported instance when blast radius shows more
