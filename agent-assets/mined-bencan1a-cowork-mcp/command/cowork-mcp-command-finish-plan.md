# Finish Plan

Complete a cowork-mcp implementation plan: verify deliverables, run all checks, write HANDOFF.md, and mark the plan complete.

**Plan:** $ARGUMENTS

## What To Do

### Step 1: Identify the Plan

Find the active plan:
- If `$ARGUMENTS` is provided: use `agent-projects/{$ARGUMENTS}/plan.md`
- Otherwise: check the current todo list for an in-progress plan, or list in-progress plans in `agent-projects/`

Ask the user if unclear.

### Step 2: Verify Deliverables

Read the plan.md and go through each listed deliverable:
- For each file listed: verify it exists
- For each stated behavior: verify it's implemented

Run the full check suite:
```bash
make check-all
```

If `make check-all` fails:
- Fix the failures
- Re-run to confirm

If a deliverable is NOT met, report it and ask the user how to proceed before continuing.

Display a checklist with pass/fail status for each deliverable.

### Step 3: Write HANDOFF.md

Create `agent-projects/{plan}/HANDOFF.md` with:

```markdown
# Handoff: {Plan Name}

**Status**: Complete
**Date**: {today's date}
**Completed by**: Claude Code

## What Was Produced

[List every file created or modified with a one-line description]

## Summary

[2-3 paragraphs: what was implemented, key design choices made, why]

## Deliverables Checklist

- [x] {deliverable 1}
- [x] {deliverable 2}
- [ ] {unmet deliverable, if any}

## Decisions Made

[Any architectural or design choices made during implementation, with rationale]

## Known Issues

[Anything that needs future attention, or known limitations]

## Next Steps

[What downstream work should know, or what to do next]
```

### Step 4: Update Plan Status

Update the `status` field in `agent-projects/{plan}/plan.md` frontmatter to `complete` and add a `completed` date field.

### Step 5: Summarize

Report to the user:
- What was completed
- Final check-all status
- Any known issues noted in HANDOFF.md
- Suggested next steps

## Notes

- Do NOT commit anything — leave that to the user
- If checks fail and can't be fixed automatically, document the failure in HANDOFF.md under "Known Issues" and ask the user how to proceed
- A partial completion is still a completion if the plan scope was narrowed — document what was done vs. what was deferred
