---
name: status-update
description: Draft the user's status update from the active project's tasks.md and recent notes in operations/. Use when the user needs to report progress to their team, their manager, or stakeholders.
---

# Status update

Draft the update the user owes someone, from files, not from their memory.

## Steps

1. **Find the state.** Read the active project's `tasks.md` (Status notes first, then Now / Next / Blocked) and any `operations/` notes dated since the last update. If several projects are active, ask which ones the update covers.
2. **Ask two things only:** who the update is for, and where it will be posted (email, Slack, a doc). Skip the questions if the conversation already says.
3. **Draft it** in the user's voice per `context/preferences.md`. Default shape, unless preferences say otherwise:
   - One line on the headline: the single most important thing that moved or didn't.
   - What shipped or progressed, with the concrete result.
   - What's blocked, with the specific ask that would unblock it. An update without an ask is a diary entry.
   - What's next.
4. **Match the channel.** Slack gets short lines and no headings; email gets a subject line; a doc gets the full shape.

## Rules

- Every claim of progress points at something real: a merged change, a decision made, a number moved, a meeting outcome. No "good progress on X".
- Blockers name the blocker, not just the feeling. "Waiting on legal's read of the data clause since the 12th" beats "legal is slow".
- After the user approves the draft, update `tasks.md`'s Status notes so the next update starts from today's truth.
