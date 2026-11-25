---
name: checkpoint-recovery
description: "Saves and restores progress checkpoints for long multi-step tasks. Trigger when: save progress, checkpoint, resume task, task interrupted, recover from interruption, where were we, 儲存進度, 斷點恢復, 繼續任務, 從哪裡繼續."
metadata:
  category: meta
  version: "1.0"
---

# Checkpoint Recovery

Saves the current state of a long-running task to a checkpoint file so it can be resumed accurately after interruption, context reset, or session end.

## Purpose

Capture a complete snapshot of in-progress task state — completed steps, current step status, remaining steps, key decisions, and created files — and restore that state precisely on resume so no work is repeated or lost.

## Trigger

Apply when:
- User says "save progress", "checkpoint", "resume task", "where were we", "recover from interruption"
- "儲存進度", "斷點恢復", "繼續任務", "從哪裡繼續"
- Task has more than 5 remaining subtasks and context window is filling up
- Approaching context window compression (proactive trigger)
- Before any operation that changes external state (file writes, API calls, database changes)
- User requests a pause or indicates they will return later

Do NOT trigger for:
- Simple tasks completable in a single turn
- Already-completed tasks with no remaining steps

## Prerequisites

- An in-progress task with defined steps
- Write access to the current working directory (for checkpoint file) or the ability to output the checkpoint in-context

## Steps

1. **Detect checkpoint need** — trigger automatically when any of the following conditions are true:
   - More than 5 subtasks remain
   - Context window is estimated above 70% full
   - User explicitly requests a save
   - About to execute an irreversible external operation

2. **Save checkpoint** — record all of the following:
   - Task name and overall goal
   - Completed steps with their outcomes (not just "done" but what was produced)
   - Current step: which step, its status, and what partial work exists
   - Remaining steps in order
   - Key decisions made and their rationale
   - All files created or modified with their paths and descriptions
   - The exact instruction needed to resume

3. **Write checkpoint file** — save to `checkpoint.md` in the current working directory; if file write is not possible, output the checkpoint block in-context so the user can save it manually

4. **On resume** — when a checkpoint is detected or the user says "resume":
   - Read the checkpoint file
   - Verify current state matches expected state: confirm each created file exists and contains the expected content; confirm external calls completed successfully
   - Report any discrepancies between checkpoint state and actual state
   - Ask the user to confirm which step to continue from before proceeding

5. **Continue execution** — resume from the confirmed step; update the checkpoint file after each completed step so it always reflects the current state; delete the checkpoint file when the task is fully complete

## Output Format

Checkpoint file saved to: `./checkpoint.md`

```markdown
## Checkpoint: <task name>

**Saved:** <timestamp>
**Status:** in-progress
**Overall goal:** <one-line goal statement>
**Done when:** <verifiable completion criterion>

### Completed Steps
1. ✅ <step description> — <outcome: what was produced or confirmed>
2. ✅ <step description> — <outcome>

### Current Step
3. 🔄 <step description> — <current status: e.g., "50% complete, modified auth.ts lines 1–45">

### Remaining Steps
4. <step description>
5. <step description>
6. <step description>

### Key Decisions
- <decision> — <rationale>
- <decision> — <rationale>

### Created / Modified Files
- `<file path>` — <description of changes>
- `<file path>` — <description of changes>

### Resume Instructions
**Continue from step 3:** <exact instruction to resume the current step>
**Verify first:** <what to check before resuming>
```

## Rules

### Must
- Save a checkpoint before any operation that changes external state (file writes, API calls, database mutations)
- Verify external state on resume — files and APIs may have changed since the checkpoint was saved
- Confirm with the user which step to resume from before executing anything
- Update the checkpoint file after each completed step
- Delete the checkpoint file when the task is fully complete

### Never
- Never resume from a checkpoint without first verifying that current state matches expected state
- Never save ephemeral UI or in-memory state as a checkpoint — only save task progress and file system state
- Never overwrite an existing checkpoint without confirming with the user that the old checkpoint is no longer needed
- Never mark a step as completed in the checkpoint unless its done-condition has been verified

## Examples

### Good Example

A refactoring task with 8 steps is interrupted at step 4. Checkpoint records: steps 1–3 modified `db.ts`, `models/user.ts`, and `migrations/001.sql`; step 4 is in-progress on `auth/jwt.ts` (first 45 lines updated). On resume, Claude reads the checkpoint, verifies the three completed files match their expected state, reports "Step 4 is partially complete — `auth/jwt.ts` lines 1–45 have been updated; lines 46–90 remain." Asks user to confirm before continuing. Proceeds to finish step 4, updates checkpoint, then continues to steps 5–8.

### Bad Example

```
OK let me pick up where we left off.
I'll start implementing the JWT logic.
```

> Why this is bad: No checkpoint was read, completed steps were not verified, and there is no confirmation of which step to resume from. Previously completed work may be duplicated, and partially completed work may be overwritten incorrectly.
