---
description: "Use for any modification to an existing bootstrapped app: new features, bug fixes, UI polish, analytics fixes, or adding tests."
type: code-writing
reads:
  - experiment/experiment.yaml
  - experiment/EVENTS.yaml
  - CLAUDE.md
stack_categories: [framework, database, auth, analytics, ui, payment, email, testing, hosting, ai, telephony, voice, notifications, project-management]
requires_approval: true
references:
  - .claude/patterns/verify.md
  - .claude/patterns/branch.md
  - .claude/patterns/observe.md
  - .claude/patterns/messaging.md
  - .claude/patterns/design.md
  - .claude/patterns/solve-reasoning.md
  - .claude/procedures/plan-exploration.md
  - .claude/procedures/plan-validation.md
  - .claude/procedures/change-plans.md
branch_prefix: change
modifies_specs: true
---
Make a change to the existing app: $ARGUMENTS

## Arguments

Parse `$ARGUMENTS` for:
- `#<number>` or bare number: read the GitHub issue via `gh issue view <number>` as the change description
- `--light`: force light solve-reasoning depth (skip deep analysis)
- `--full`: force full solve-reasoning depth (deep analysis regardless of complexity)
- Everything else: the change description in natural language

ARGUMENTS: $ARGUMENTS

## Mode Detection

Before entering the lifecycle, check `.runs/current-plan.md`:

- If it exists with frontmatter `skill: change` and a `checkpoint` field → **resume** mode. The lifecycle engine skips already-completed states automatically. State the detected checkpoint: "Resuming at **[checkpoint]**."
- If it does not exist → **fresh** mode.

## Lifecycle

0. Opportunistically clean >24h stale change worktrees (skips active sessions):
   ```bash
   bash .claude/scripts/lib/clean-stale-worktrees.sh change
   ```
1. Enter worktree isolation (conditional — only when not already isolated):
   a. Detect existing isolation:
      ```bash
      IN_WORKTREE=$(bash .claude/scripts/lib/in-worktree.sh)
      ```
   b. If `IN_WORKTREE=false`:
      - Call `EnterWorktree` with name `"change-<current-timestamp>"`
      - On success: run `mkdir -p .runs` then `npm ci`; set `WORKTREE_OWNER=true`
      - On failure: continue in current directory; set `WORKTREE_OWNER=false`
   c. If `IN_WORKTREE=true`:
      - Skip `EnterWorktree` (the parent session owns this worktree)
      - Set `WORKTREE_OWNER=false`
2. Run `bash .claude/scripts/lifecycle-init.sh change '{"skill":"change"}'`, then merge worktree_owner into the context (reuses init-context.sh's has_identity merge path):
   ```bash
   bash .claude/scripts/init-context.sh change "{\"worktree_owner\": $WORKTREE_OWNER}"
   ```
3. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh change)`
   b. If NEXT is "FINALIZE" → go to step 4
   c. If NEXT starts with "EMBED_COMPLETE:" → parse the suffix as `<skill>:<state>`, run `bash .claude/scripts/advance-state.sh <skill> <state>`, then return to step 3a
   d. If NEXT does not start with "/" → STOP with error (print NEXT for diagnosis)
   e. Read the state file at $NEXT and execute its ACTIONS section
   f. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   g. Return to step 3a
4. Conditional cleanup (only when this skill owns the worktree):
   ```bash
   OWNER=$(python3 -c "import json; print(str(json.load(open('.runs/change-context.json')).get('worktree_owner', False)).lower())")
   ```
   If `OWNER=true`:
   a. Run `bash .claude/scripts/lifecycle-worktree-sync.sh`
   b. Call `ExitWorktree` with action `"remove"` and `discard_changes: true`
   Else: skip cleanup. The parent session owns the worktree, OR the context predates this fix and may need one-time manual cleanup.

**Note:** STATE 7 (USER_APPROVAL) pauses for user input. The lifecycle loop resumes when the user responds with approval.

## Do NOT
- Add more than what `$ARGUMENTS` describes — one change per PR
- Modify existing behaviors unless the change requires integration (e.g., adding a nav link)
- Remove or break existing analytics events (unless the change is specifically about fixing analytics)
- Add libraries not in experiment.yaml `stack` without user approval
- Skip updating experiment.yaml when adding new behaviors — the source of truth must always reflect the current app
- Change analytics event names — they must match experiment/EVENTS.yaml
- Add analytics events without user approval
- Add error-state tests — funnel tests cover the happy path only
- Mock services in tests — the whole point is testing real integrations
- Skip Step 7 verification (verify.md must run with the classified scope — build loop and auto-observe always run; review agents run per scope)
- Commit to main directly
