---
name: lifekernel-morning-plan
description: Run a five-minute morning opening that picks today's focus from last night's plan, due tasks, and fixed commitments, within realistic capacity.
---

# Morning plan

Run only when the user starts it ("good morning", "let's plan the day") or accepts an offer you made because `ritual_status` showed it due. Keep it to about five minutes. Converse in the user's language.

## Before talking

1. Call `vault_list`, pick the personal vault, then call `context_bundle`.
2. If `system/Method.md` is blank, say the vault has not been onboarded and offer the onboarding skill.
3. Call `ritual_agenda` with `ritual: "morning-plan"`. It returns yesterday's focus and open loops, the plan's focus for today, overdue and due tasks, and today's fixed commitments, each with its source note.
4. If `yesterday.circle` is empty, offer a two-minute catch-up of yesterday first (the daily-circle skill, shortened). Accept a no without comment.

## The conversation

Show a compact picture: the focus planned last night, what is due or overdue, and today's fixed commitments. Ask what the user wants to make true today. Help them choose one main focus and at most two supporting items that fit the time left around commitments and the buffer in `schedule/Capacity.md`.

If `inbox.count` is above zero, mention the number and ask whether any captured item belongs in today's plan; full triage waits for the evening circle unless the user wants it now.

Overdue tasks are choices, not debts. For the ones that matter, ask whether to do, reschedule, or drop them. Do not plan every hour unless the method uses time blocks. Do not add goals or outside commitments.

## Recording

- **Daily note.** If `todayNote` is null, create today's note on the `daily` route with the daily template sections and fill "Plan for today". If it exists, use `update_section` on "Plan for today" with `todayNote.sha256`.
- **Completion.** Set `morning_plan: "done"`, in `fields` when you create the note or with `set_frontmatter` when it exists. If the user skips the morning plan, set `morning_plan: "skipped"`.
- **Tasks.** Change a rescheduled task's due date in its canonical project or area note with `update_section`. Mark a task cancelled (`- [-]`) only when the user says to drop it.
- Follow the write protocol in the daily-circle skill.

Close with today's focus in one line.
