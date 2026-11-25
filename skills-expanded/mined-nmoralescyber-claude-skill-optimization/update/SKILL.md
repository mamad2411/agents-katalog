---
name: update
description: DEPRECATED as of 2026-04-25 — overlaps with personal-assistant, which already handles task sync and memory refresh from email, calendar, and chat. Use personal-assistant for daily sync and productivity:task-management for direct backlog edits.
---

# DEPRECATED: update

This skill has been deprecated for a solo cybersecurity-focused founder/operator workflow.

## Reason for deprecation

`update` exists to pull new tasks from your project tracker, triage stale items, and refresh memory — but `personal-assistant` already does this end-to-end as part of the morning briefing, end-of-day recap, and ad-hoc "check my email / what's on my plate" flows. Running both produces duplicate scans of the same inboxes and conflicting writes to `TASKS.md`. Consolidating on `personal-assistant` removes the overlap and keeps task sync inside the assistant loop you already use daily.

## Use these alternatives instead

| Need | Skill |
|---|---|
| Sync tasks and refresh memory from email, calendar, chat, mail | `personal-assistant` |
| Directly add, complete, or reorganize tasks in `TASKS.md` | `productivity:task-management` |

## Restoration

If your role changes (e.g., you stop using personal-assistant, or you want a dedicated tracker-only sync skill that doesn't touch email/calendar), restore the original from the originally-installed plugin location, or remove this stub from `~/.claude/skills/update/SKILL.md` so the original takes precedence.
