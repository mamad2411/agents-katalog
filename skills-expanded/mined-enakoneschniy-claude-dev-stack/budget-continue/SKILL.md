---
name: budget-continue
description: >
  Show 4-option continuation prompt when session budget is low. Options: remind later (CronCreate),
  auto-continue locally (Desktop task), auto-continue in cloud (Cloud task), continue now.
  Trigger when: budget warning fires, session limit reached, context is full, user sees budget warning.
trigger: budget low, session limit, context full, budget warning, budget continue
---

# Budget Continue Skill

When the session budget warning fires, this skill presents a 4-option continuation menu and (when invoked inside a Claude Code session) can schedule the appropriate follow-up action using native Claude Code tools.

## Invocation

```
claude-dev-stack budget continue
```

Or invoke this skill directly: `/budget-continue`

## The 4 Options

### Option 1: Remind me later (CronCreate)

Creates a one-shot CronCreate reminder that fires in the current Claude Code session after a delay.

When the user selects this option inside a Claude Code session:

```
Use CronCreate to schedule a reminder:
  Title:    "Resume GSD session — budget warning"
  Prompt:   "/budget-continue"
  Schedule: "+1h"  (or user-chosen delay)
  Repeat:   false
```

### Option 2: Auto-continue locally (Desktop task)

Creates a Desktop task that fires on the local machine after a delay and runs the GSD resume workflow.

When the user selects this option inside a Claude Code session:

```
Use the Desktop task tool:
  Prompt:   "/gsd-resume-work"
  Schedule: "+1h"  (or user-chosen delay)
```

Note: The machine must be on when the task fires. STATE.md is read to determine what to resume.

### Option 3: Auto-continue in cloud (Cloud task)

Creates a Cloud task that runs on Anthropic infrastructure. Performs a fresh git clone and runs the GSD resume workflow autonomously — works even when the local machine is off.

When the user selects this option inside a Claude Code session:

```
Use the Cloud task tool:
  Repo:     (git remote origin URL — auto-detected)
  Prompt:   "/gsd-resume-work"
  Schedule: "+1h"  (or user-chosen delay)
```

Note: All state must be committed to git. GSD guarantees this via STATE.md.

### Option 4: Continue now

No scheduling action. Prints a message to continue with the current session.
Useful if the user decides to keep working and address the budget limit later.

## What the scheduled task runs

Both Desktop and Cloud tasks run `/gsd-resume-work`, which reads `.planning/STATE.md`:
- If `stopped_at` is present: resumes from that point using `resume_file` as context
- If no stopped work: runs maintenance tasks (check PRs, `/gsd-next`, `/gsd-health`)

The `loop.md` template (if installed to `.claude/loop.md`) provides the full maintenance loop instructions for scheduled tasks.

## Notes

- Hooks cannot interactively invoke Claude Code tools — hence the CLI command for manual invocation.
- When invoked as a skill inside a Claude Code session, scheduling tools (CronCreate, Desktop, Cloud) are directly available.
- The budget warning message includes: `Run: claude-dev-stack budget continue` as a reminder.
