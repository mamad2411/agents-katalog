# Start Plan

Load context for a cowork-mcp implementation plan and prepare to begin work.

**Plan:** $ARGUMENTS

## What To Do

### Step 1: Identify the Plan

Find the plan at `agent-projects/{$ARGUMENTS}/plan.md`.

If `$ARGUMENTS` is not provided, list all plans in `agent-projects/` with their status and ask the user which to start.

### Step 2: Check Status

Read `agent-projects/{plan}/plan.md` and check the frontmatter `status` field:
- If `status: complete` → STOP and report "This plan is already complete."
- If `status: in-progress` → Note that you're resuming, continue
- If `status: pending` or `status: draft` → Proceed to start

### Step 3: Load Context

Read the plan file in full, then read the files it references. Based on the plan content, read the relevant source files. Common references to read:
- `server.py` — if the plan touches tool registration
- `auth/token_store.py` — if the plan touches auth
- `graph/client.py` — if the plan touches Graph API
- `config.py` — if the plan touches settings
- Relevant `graph/*.py` — if the plan touches specific Graph domains

### Step 4: Check for HANDOFF.md

If `agent-projects/{plan}/HANDOFF.md` exists, read it. It documents what was completed in a prior session and what remains. Use it to orient yourself.

### Step 5: Update Status

Update the plan.md frontmatter to set `status: in-progress` (if not already set).

### Step 6: Report

Summarize to the user:
- **Goal**: What this plan delivers
- **Already done**: What HANDOFF.md says was completed (if anything)
- **Next step**: The first concrete action to take based on the plan

## Notes

- Plans live in `agent-projects/<plan-name>/plan.md`
- HANDOFF.md (if present) is the record from the previous session — trust it
- The plan.md frontmatter uses: `status`, `owner`, `created`, `summary`
